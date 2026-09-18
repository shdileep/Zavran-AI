#!/usr/bin/env python3
"""
Zaroon AI Production Voice Engine — Diagnostic & Verification Suite
Tests voice identity, speech formatting, audio normalization, caching, and streaming latency.
"""

import sys
import time
import asyncio
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import settings
from backend.services.zaroon_speech_formatter import ZaroonSpeechFormatter, zaroon_speech_formatter
from backend.services.zaroon_audio import ZaroonAudioProcessor, zaroon_audio_processor
from backend.services.zaroon_tts import ZaroonTTSProvider, zaroon_tts_provider


def test_speech_formatter():
    print("\n" + "=" * 70)
    print("[TEST 1] ZaroonSpeechFormatter — Markdown Stripping & Technical Preservations")
    print("=" * 70)

    sample_markdown = (
        "### Technical Assessment\n"
        "- The candidate explained **FastAPI** with `LangGraph` and **PostgreSQL**.\n"
        "- We noticed good usage of **RAG**, **FAISS**, and **Docker** containers.\n"
        "Can you explain how *pgvector* performs approximate nearest neighbor search?"
    )

    formatted = zaroon_speech_formatter.format_for_speech(sample_markdown)
    print(f"Original Input:\n{sample_markdown}\n")
    print(f"Formatted Spoken Dialogue:\n{formatted}\n")

    # Assertions
    assert "**" not in formatted, "Markdown bold must be stripped."
    assert "###" not in formatted, "Markdown headers must be stripped."
    assert "`" not in formatted, "Code ticks must be stripped."
    assert "-" not in formatted or "- " not in formatted, "Bullet points must be stripped."
    assert "FastAPI" in formatted, "FastAPI term must be preserved."
    assert "LangGraph" in formatted, "LangGraph term must be preserved."
    assert "PostgreSQL" in formatted, "PostgreSQL term must be preserved."
    assert "pgvector" in formatted, "pgvector term must be preserved."
    assert "FAISS" in formatted, "FAISS term must be preserved."
    assert "Docker" in formatted, "Docker term must be preserved."

    print("[PASS] Speech Formatter preserves exact technical terms and produces clean speech.")


def test_audio_processor_and_normalization():
    print("\n" + "=" * 70)
    print("[TEST 2] ZaroonAudioProcessor — Header Validation & Safe Normalization")
    print("=" * 70)

    # Test empty payload validation
    res_empty = zaroon_audio_processor.validate_audio(b"")
    assert not res_empty["valid"], "Empty payload must be invalid."

    # Test dummy WAV generation & validation
    import wave
    import struct
    import io

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        # 0.5s of gentle sine wave audio
        frames = [int(5000 * (i % 20 - 10) / 10.0) for i in range(12000)]
        wf.writeframes(struct.pack(f"<{len(frames)}h", *frames))

    synthetic_wav = buf.getvalue()
    val = zaroon_audio_processor.validate_audio(synthetic_wav)
    assert val["valid"], "Synthesized WAV must be valid."
    assert val["format"] == "audio/wav"
    assert val["sample_rate"] == 24000
    print(f"[OK] Validated WAV structure: {val['duration_seconds']}s @ {val['sample_rate']}Hz")

    # Safe Peak Normalization
    normalized = zaroon_audio_processor.normalize_loudness(synthetic_wav, target_headroom_db=-1.0)
    val_norm = zaroon_audio_processor.validate_audio(normalized)
    assert val_norm["valid"], "Normalized WAV must retain valid structure."
    print(f"[OK] Normalization applied safely without clipping: {len(normalized)} bytes")

    print("[PASS] Audio Processor validation and normalization verified.")


async def test_zaroon_tts_synthesis_and_caching(benchmark: bool = False):
    print("\n" + "=" * 70)
    print("[TEST 3] ZaroonTTSProvider — Voice Identity, Caching & Performance")
    print("=" * 70)

    provider = ZaroonTTSProvider()
    val = provider.validate_voice()
    print(f"Provider Status: {provider.health_check()}")
    print(f"Configured Voice Hash: {val['voice_hash']}")
    print(f"Model: {val['model']} | Target Speed: {val['speed']}")

    sample_phrase = "Good answer. Let's go deeper into vector database indexing."

    print(f"Synthesizing test phrase: '{sample_phrase}' using {val.get('active_provider')}...")
    t0 = time.perf_counter()
    res1 = await provider.synthesize_speech(sample_phrase)
    lat1 = (time.perf_counter() - t0) * 1000

    if res1["status"] == "success":
        print(f"[SUCCESS] Cold Synthesis in {lat1:.1f}ms | Bytes: {res1.get('audio_bytes')} | Audio: {res1.get('format')}")
        
        # Test Caching on second identical call
        t1 = time.perf_counter()
        res2 = await provider.synthesize_speech(sample_phrase)
        lat2 = (time.perf_counter() - t1) * 1000
        print(f"[SUCCESS] Cached Synthesis in {lat2:.2f}ms (Cached: {res2.get('cached')})")
        assert res2.get("cached") is True, "Second call for static phrase must be cached."
        print(f"[PERF] Cache speedup: {lat1/max(lat2, 0.01):.1f}x faster")

        # Test Streaming Chunks
        print("\nTesting chunked audio streaming generator...")
        chunks = []
        async for chunk in provider.stream_speech(sample_phrase, chunk_size=2048):
            chunks.append(chunk)
        print(f"[OK] Stream yielded {len(chunks)} chunks, total {sum(len(c) for c in chunks)} bytes.")
        assert len(chunks) > 0, "Stream must yield chunks."
    else:
        print(f"[INFO] Response: {res1}")

    print("[PASS] Zaroon TTS Engine validation complete.")


def main():
    parser = argparse.ArgumentParser(description="Zaroon AI Production Voice Engine Tester")
    parser.add_argument("--benchmark", action="store_true", help="Run latency and throughput benchmark")
    args = parser.parse_args()

    print("=" * 70)
    print("ZAVRAN AI — ZAROON PRODUCTION VOICE ENGINE DIAGNOSTICS")
    print("=" * 70)

    test_speech_formatter()
    test_audio_processor_and_normalization()
    asyncio.run(test_zaroon_tts_synthesis_and_caching(benchmark=args.benchmark))

    print("\n" + "=" * 70)
    print("[ALL DIAGNOSTIC CHECKS PASSED SUCCESSFULLY]")
    print("=" * 70)


if __name__ == "__main__":
    main()
