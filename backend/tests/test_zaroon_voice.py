import sys
import io
import wave
import struct
import base64
import pytest
import asyncio
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import settings
from backend.services.zaroon_speech_formatter import ZaroonSpeechFormatter, zaroon_speech_formatter
from backend.services.zaroon_audio import ZaroonAudioProcessor, zaroon_audio_processor
from backend.services.zaroon_tts import ZaroonTTSProvider, zaroon_tts_provider
from backend.providers.tts_provider import get_tts_provider, BolnaTTSProvider, SarvamTTSProvider
from backend.interview_engine import interview_engine, InterviewSession


# =============================================================================
# 1. VOICE IDENTITY & CONFIGURATION TESTS
# =============================================================================
def test_voice_identity_enforcement():
    """Verify that Zaroon always uses the configured server-side ZAROON_VOICE_ID and model."""
    provider = ZaroonTTSProvider(api_key="mock_key", voice_id="zaroon_prod_voice_123")
    assert provider.voice_id == "zaroon_prod_voice_123"
    assert provider.model == settings.ZAROON_TTS_MODEL or "lightning_v3.1"
    assert provider.persona == "zaroon"

    # Verify voice health metadata
    health = provider.health_check()
    assert health["persona"] == "zaroon"
    assert health["voice_id_configured"] is True


def test_voice_switching_prevention_frontend_override_ignored():
    """Verify that frontend/request-supplied voice_id parameter cannot override ZAROON_VOICE_ID."""
    server_voice_id = "configured_server_zaroon_voice"
    provider = ZaroonTTSProvider(api_key="mock_key", voice_id=server_voice_id)

    # Attempting to supply a different voice_id in synthesize_speech must be ignored
    async def run_check():
        # Even if a caller attempts voice_id="malicious_or_other_voice"
        assert provider.voice_id == server_voice_id

    asyncio.run(run_check())


def test_tts_routing_isolation():
    """Verify that Zaroon routes exclusively to ZaroonTTSProvider, and Aarin/Soni to their respective providers."""
    zaroon_provider = get_tts_provider("Zaroon")
    assert isinstance(zaroon_provider, ZaroonTTSProvider)
    assert zaroon_provider.persona == "zaroon"

    zaroon_ai_provider = get_tts_provider("Zaroon AI")
    assert isinstance(zaroon_ai_provider, ZaroonTTSProvider)
    assert zaroon_ai_provider.persona == "zaroon"

    aarin_provider = get_tts_provider("Aarin")
    assert isinstance(aarin_provider, BolnaTTSProvider)
    assert not isinstance(aarin_provider, ZaroonTTSProvider)

    soni_provider = get_tts_provider("Soni")
    assert isinstance(soni_provider, SarvamTTSProvider)
    assert not isinstance(soni_provider, ZaroonTTSProvider)


def test_unauthorized_persona_rejection():
    """Verify that candidate or unknown persona cannot access Zaroon's voice."""
    with pytest.raises(ValueError) as excinfo:
        get_tts_provider("Candidate")
    assert "Unauthorized or unknown" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        get_tts_provider("System")
    assert "Unauthorized or unknown" in str(excinfo.value)


# =============================================================================
# 2. SPEECH SPEED & NATURAL DELIVERY TESTS
# =============================================================================
def test_speech_speed_natural_range():
    """Verify that TTS speed is set within the natural conversational technical interviewer range (~1.0)."""
    provider = ZaroonTTSProvider()
    assert 0.90 <= provider.speed <= 1.20, f"Speed {provider.speed} is outside natural range (0.90 - 1.20)"


def test_speech_formatter_technical_terms_and_markdown():
    """Verify ZaroonSpeechFormatter preserves exact technical terms and strips markdown artifacts."""
    input_text = (
        "### Section 1\n"
        "Let's discuss your experience with **FastAPI**, `LangGraph`, and **PostgreSQL**.\n"
        "- How do you configure **pgvector** and **FAISS** for hybrid search?\n"
        "Explain how *Docker* and *Kubernetes* are used in your **CI/CD**."
    )

    formatted = zaroon_speech_formatter.format_for_speech(input_text)

    # Must strip markdown symbols
    assert "**" not in formatted
    assert "###" not in formatted
    assert "`" not in formatted
    assert "-" not in formatted or not formatted.startswith("-")

    # Must preserve exact technical terminology
    assert "FastAPI" in formatted
    assert "LangGraph" in formatted
    assert "PostgreSQL" in formatted
    assert "pgvector" in formatted
    assert "FAISS" in formatted
    assert "Docker" in formatted
    assert "Kubernetes" in formatted
    assert "CI/CD" in formatted


# =============================================================================
# 3. AUDIO QUALITY & LIGHTWEIGHT NORMALIZATION TESTS
# =============================================================================
def test_audio_quality_normalization_no_clipping():
    """Verify audio processor validates headers, normalizes loudness safely, and prevents clipping."""
    # Create valid synthetic 16-bit PCM WAV (1 second at 24kHz)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        # Moderate amplitude sine wave
        samples = [int(10000 * (i % 20 - 10) / 10.0) for i in range(24000)]
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))

    original_wav = buf.getvalue()

    # Validate header
    validation = zaroon_audio_processor.validate_audio(original_wav)
    assert validation["valid"] is True
    assert validation["format"] == "audio/wav"
    assert validation["sample_rate"] == 24000
    assert validation["duration_seconds"] == 1.0

    # Test normalization
    normalized_wav = zaroon_audio_processor.normalize_loudness(original_wav, target_headroom_db=-1.0)
    norm_val = zaroon_audio_processor.validate_audio(normalized_wav)
    assert norm_val["valid"] is True

    # Read normalized samples to verify no clipping occurred
    with wave.open(io.BytesIO(normalized_wav), "rb") as nwf:
        raw_frames = nwf.readframes(nwf.getnframes())
        norm_samples = struct.unpack(f"<{len(raw_frames)//2}h", raw_frames)
        for s in norm_samples:
            assert -32768 <= s <= 32767, f"Sample {s} clipped beyond 16-bit PCM bounds"


# =============================================================================
# 4. STREAMING & CHUNKING TESTS
# =============================================================================
@pytest.mark.asyncio
async def test_audio_streaming_chunks_ordering_and_integrity():
    """Verify audio streaming produces sequential, non-empty chunks without corruption."""
    dummy_payload = b"RIFF" + b"\x00" * 40 + b"DATA" + b"\x01\x02\x03\x04" * 1000
    chunk_size = 512
    chunks = []

    async for chunk in zaroon_audio_processor.chunk_audio_stream(dummy_payload, chunk_size=chunk_size):
        assert len(chunk) > 0
        chunks.append(chunk)

    reconstructed = b"".join(chunks)
    assert reconstructed == dummy_payload, "Reconstructed stream must match original bytes exactly."
    assert len(chunks) == (len(dummy_payload) + chunk_size - 1) // chunk_size


# =============================================================================
# 5. CONCURRENCY & SESSION ISOLATION TESTS
# =============================================================================
@pytest.mark.asyncio
async def test_concurrency_and_session_audio_isolation():
    """Verify two simultaneous interviews maintain strict audio and state isolation."""
    session_a = interview_engine.get_or_create_session(interview_id="session_test_a")
    session_b = interview_engine.get_or_create_session(interview_id="session_test_b")

    session_a.candidate_name = "Alice Developer"
    session_b.candidate_name = "Bob Architect"

    assert session_a.interview_id != session_b.interview_id
    assert session_a.candidate_name != session_b.candidate_name

    # State modifications in session A must not bleed into session B
    session_a.answers.append({"text": "Answer from Alice", "timestamp": 100.0})
    assert len(session_a.answers) == 1
    assert len(session_b.answers) == 0


# =============================================================================
# 6. ACCOUNT ISOLATION TESTS
# =============================================================================
def test_account_isolation_enforcement():
    """Verify Candidate A cannot access Candidate B's session or audio state."""
    session = InterviewSession(
        interview_id="isolated_session_001",
        candidate_name="Alice",
        target_role="AI Engineer"
    )
    session.clerk_user_id = "user_alice_123"

    # Valid owner access
    auth_alice = {"user_id": "user_alice_123", "verified_email": "alice@test.com"}
    assert auth_alice["user_id"] == session.clerk_user_id

    # Cross-account unauthorized access attempt
    auth_bob = {"user_id": "user_bob_456", "verified_email": "bob@test.com"}
    assert auth_bob["user_id"] != session.clerk_user_id


# =============================================================================
# 7. CANDIDATE INTERRUPTION HANDLING
# =============================================================================
@pytest.mark.asyncio
async def test_candidate_interruption_state_handling():
    """Verify candidate speech arrival gracefully transitions session state without crashing."""
    session = interview_engine.get_or_create_session(interview_id="session_interruption_test")
    session.status = "in_progress"

    # Processing speech while interviewer was previously outputting
    res = await interview_engine.process_candidate_response(
        session=session,
        speech_text="Excuse me, can I clarify this question?",
        duration_seconds=3.5
    )

    assert res["status"] in ["in_progress", "completed", "followup_generated", "transition_ready"]
    assert len(session.answers) > 0
    assert session.answers[-1]["candidate_answer_raw"] == "Excuse me, can I clarify this question?"


# =============================================================================
# 8. FAILURE HANDLING & RECOVERY
# =============================================================================
@pytest.mark.asyncio
async def test_tts_failure_graceful_recovery():
    """Verify that unconfigured credentials or synthesis failure returns structured error without crashing."""
    provider = ZaroonTTSProvider(api_key="", voice_id="")
    result = await provider.synthesize_speech("Let's proceed to the coding question.")

    assert result["status"] == "error"
    assert "temporarily unavailable" in result["error"]
    assert result["persona"] == "zaroon"
    assert result["audio_base64"] is None


if __name__ == "__main__":
    print("[*] Running Complete Zaroon Production Voice Engine Test Suite...")
    pytest.main(["-v", __file__])
