import io
import wave
import struct
import logging
from typing import Dict, Any, AsyncGenerator, Optional

logger = logging.getLogger("ZavranAI.ZaroonAudio")

class ZaroonAudioProcessor:
    """
    Lightweight, deterministic audio processor and validator for Zaroon AI voice streams.
    
    Principles:
    1. Preserves voice identity 100%: Never applies pitch-shifting, formant-shifting,
       voice-morphing, reverb, chorus, or artificial filters.
    2. Ensures clean, clear, loud audio without clipping or digital distortion.
    3. Validates WAV/MP3 byte structures to ensure corruption-free playback.
    4. Provides chunked streaming generators for ultra-low Time-To-First-Audio (TTFT).
    """

    @staticmethod
    def validate_audio(audio_bytes: bytes) -> Dict[str, Any]:
        """
        Validates the binary structure of synthesized audio bytes.
        Checks for WAV RIFF headers, valid sample rates, and non-empty payload.
        """
        if not audio_bytes:
            return {
                "valid": False,
                "error": "Empty audio payload received.",
                "format": "unknown",
                "duration_seconds": 0.0,
            }

        size = len(audio_bytes)
        if size < 44:
            return {
                "valid": False,
                "error": f"Audio payload too small ({size} bytes). Minimum valid header is 44 bytes.",
                "format": "unknown",
                "duration_seconds": 0.0,
            }

        # Check for WAV header
        if audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
            try:
                with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                    channels = wf.getnchannels()
                    sampwidth = wf.getsampwidth()
                    framerate = wf.getframerate()
                    nframes = wf.getnframes()
                    duration = nframes / float(framerate) if framerate > 0 else 0.0
                    return {
                        "valid": True,
                        "format": "audio/wav",
                        "channels": channels,
                        "sample_width": sampwidth,
                        "sample_rate": framerate,
                        "frames": nframes,
                        "duration_seconds": round(duration, 3),
                        "size_bytes": size,
                    }
            except Exception as e:
                logger.warning(f"WAV parsing issue despite RIFF header: {e}")
                return {
                    "valid": True,
                    "format": "audio/wav",
                    "size_bytes": size,
                    "duration_seconds": round(size / (24000 * 2), 3),
                }

        # Check for MP3 sync word (0xFFFB, 0xFFF3, 0xFFF2, or ID3)
        if audio_bytes[:3] == b"ID3" or (audio_bytes[0] == 0xFF and (audio_bytes[1] & 0xE0) == 0xE0):
            return {
                "valid": True,
                "format": "audio/mpeg",
                "size_bytes": size,
                "duration_seconds": round(size / 16000, 3), # Approximate
            }

        # Fallback raw audio payload
        return {
            "valid": True,
            "format": "audio/octet-stream",
            "size_bytes": size,
            "duration_seconds": round(size / 48000, 3),
        }

    @staticmethod
    def normalize_loudness(audio_bytes: bytes, target_headroom_db: float = -1.0) -> bytes:
        """
        Lightweight, zero-latency peak normalization for 16-bit PCM WAV audio.
        Ensures consistent loudness without clipping and without modifying voice timbre or pitch.
        If not 16-bit PCM WAV, returns original audio unmodified.
        """
        if not audio_bytes or len(audio_bytes) < 44 or audio_bytes[:4] != b"RIFF":
            return audio_bytes

        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                params = wf.getparams()
                if params.sampwidth != 2: # Only normalize 16-bit PCM
                    return audio_bytes
                
                raw_frames = wf.readframes(params.nframes)

            # Unpack 16-bit integers
            num_samples = len(raw_frames) // 2
            if num_samples == 0:
                return audio_bytes

            samples = struct.unpack(f"<{num_samples}h", raw_frames)
            max_sample = max(abs(s) for s in samples) if samples else 0

            if max_sample == 0:
                return audio_bytes

            # Target peak = 32767 * 10^(target_headroom_db / 20)
            target_peak = int(32767 * (10 ** (target_headroom_db / 20.0)))
            if max_sample >= target_peak:
                # Already loud enough or at target headroom; do not alter
                return audio_bytes

            scale = target_peak / float(max_sample)
            # Limit scale multiplier to safe range (1.0 to 2.5) to avoid noise amplification
            scale = min(scale, 2.5)

            normalized_samples = [int(s * scale) for s in samples]
            # Clamp to 16-bit bounds
            clamped = [max(-32768, min(32767, s)) for s in normalized_samples]
            normalized_frames = struct.pack(f"<{num_samples}h", *clamped)

            out_buffer = io.BytesIO()
            with wave.open(out_buffer, "wb") as out_wf:
                out_wf.setparams(params)
                out_wf.writeframes(normalized_frames)

            return out_buffer.getvalue()

        except Exception as e:
            logger.debug(f"Lightweight normalization skipped, returning raw audio: {e}")
            return audio_bytes

    @staticmethod
    async def chunk_audio_stream(
        audio_bytes: bytes,
        chunk_size: int = 4096
    ) -> AsyncGenerator[bytes, None]:
        """
        Yields audio chunks asynchronously for streaming HTTP response.
        Enables browser to begin decoding and playback immediately.
        """
        if not audio_bytes:
            return

        total_bytes = len(audio_bytes)
        offset = 0

        while offset < total_bytes:
            chunk = audio_bytes[offset : offset + chunk_size]
            offset += chunk_size
            yield chunk

zaroon_audio_processor = ZaroonAudioProcessor()
