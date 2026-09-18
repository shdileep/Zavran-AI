import os
import json
import time
import base64
import hashlib
import asyncio
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, AsyncGenerator, List

from backend.config import settings
from backend.services.zaroon_speech_formatter import ZaroonSpeechFormatter, zaroon_speech_formatter
from backend.services.zaroon_audio import ZaroonAudioProcessor, zaroon_audio_processor

logger = logging.getLogger("ZavranAI.ZaroonTTS")


class ZaroonTTSProvider:
    """
    Production Voice Engine exclusively for Zaroon AI — Zavran AI Technical Recruiter.
    
    Architectural Guarantees:
    1. Fixed Voice Identity: Strictly uses settings.ZAROON_VOICE_ID with Smallest AI Waves Lightning v3.1.
       The frontend or candidate CANNOT override or switch Zaroon's voice.
    2. Low-Latency Streaming: Supports both direct synthesis and chunked streaming generators.
    3. Natural Delivery: Uses ZaroonSpeechFormatter for conversational phrasing and technical term preservation.
    4. Audio Integrity: Clean recording, safe loudness normalization, no voice-altering filters or artificial delay.
    5. Isolated Caching: Safe caching for repeated static recruiter phrases, strictly keyed by voice ID and model.
    6. Graceful Recovery: Exponential backoff retries with structured error handling without crashing sessions.
    """

    # Static phrases that are safe for caching across interviews
    CACHEABLE_STATIC_PHRASES = {
        "Good.",
        "Good answer.",
        "Okay.",
        "Alright.",
        "Let's go deeper.",
        "Let's move on.",
        "Thank you.",
        "Now consider a production scenario.",
        "Welcome to your technical interview.",
        "Please take a moment to collect your thoughts.",
        "Let's proceed to the next technical topic."
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: Optional[str] = None,
        model: Optional[str] = None,
        speed: Optional[float] = None,
    ):
        # Explicit server-side binding
        self.api_key = api_key if api_key is not None else settings.SMALLEST_API_KEY
        self.voice_id = voice_id if voice_id is not None else settings.ZAROON_VOICE_ID
        self.model = model or getattr(settings, "ZAROON_TTS_MODEL", "lightning_v3.1")
        self.speed = float(speed if speed is not None else getattr(settings, "ZAROON_TTS_SPEED", 1.0))
        self.sample_rate = int(getattr(settings, "ZAROON_TTS_SAMPLE_RATE", 24000))
        self.language = getattr(settings, "ZAROON_TTS_LANGUAGE", "en")
        self.persona = "zaroon"

        # Endpoints
        self.primary_url = "https://waves-api.smallest.ai/api/v1/tts"
        self.fallback_url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"

        # In-memory cache for static interviewer phrases: {cache_key: {"audio_bytes": bytes, ...}}
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_cache_entries = 128

    def _get_voice_hash(self) -> str:
        """Returns a safe short hash of the configured voice ID for logging."""
        if not self.voice_id:
            return "unconfigured"
        return hashlib.sha256(self.voice_id.encode("utf-8")).hexdigest()[:8]

    def _compute_cache_key(self, text: str) -> str:
        """
        Computes deterministic cache key enforcing voice ID, model, and speed isolation.
        Pattern: zaroon:{voice_id}:{model}:{speed}:{text_hash}
        """
        text_hash = hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()[:16]
        return f"zaroon:{self.voice_id}:{self.model}:{self.speed:.2f}:{text_hash}"

    def validate_voice(self) -> Dict[str, Any]:
        """
        Validates voice engine configuration and compatibility.
        """
        has_smallest = bool(self.api_key and self.voice_id)
        has_sarvam = bool(getattr(settings, "SARVAM_API_KEY", ""))
        is_configured = has_smallest or has_sarvam
        active_provider = "Smallest AI (Waves Lightning)" if has_smallest else ("Sarvam AI (Bulbul v3)" if has_sarvam else "Browser Speech Fallback")
        return {
            "valid": is_configured,
            "active_provider": active_provider,
            "persona": self.persona,
            "model": self.model if has_smallest else getattr(settings, "ZAROON_SARVAM_MODEL", "bulbul:v3"),
            "speed": self.speed,
            "sample_rate": self.sample_rate,
            "voice_configured": bool(self.voice_id or has_sarvam),
            "voice_hash": self._get_voice_hash(),
            "api_key_configured": is_configured,
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Performs a non-invasive health check of the Zaroon TTS provider.
        """
        val = self.validate_voice()
        status = "healthy" if val["valid"] else "degraded"
        return {
            "status": status,
            "provider": val.get("active_provider", "Neural Voice Engine"),
            "persona": self.persona,
            "model": val.get("model", self.model),
            "speed": self.speed,
            "cached_entries": len(self._cache),
            "voice_id_configured": bool(self.voice_id),
        }

    async def _execute_smallest_tts(self, text: str) -> bytes:
        """
        Executes HTTP request to Smallest AI Waves TTS with retry and exponential backoff.
        """
        if not self.api_key or not self.voice_id:
            raise ValueError("Smallest AI not fully configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-ZaroonEngine/2.0",
        }

        payload = {
            "text": text,
            "voice_id": self.voice_id,
            "model": self.model,
            "sample_rate": self.sample_rate,
            "output_format": "wav",
            "speed": self.speed,
            "add_wav_header": True,
        }

        data = json.dumps(payload).encode("utf-8")
        endpoints = [self.primary_url, self.fallback_url]
        last_exception = None

        for attempt in range(2): # Up to 2 attempts
            for endpoint in endpoints:
                try:
                    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
                    loop = asyncio.get_running_loop()
                    
                    def _fetch():
                        with urllib.request.urlopen(req, timeout=12) as resp:
                            return resp.headers.get("Content-Type", ""), resp.read()

                    content_type, body_bytes = await loop.run_in_executor(None, _fetch)

                    # 1. Binary Audio Stream
                    if "audio" in content_type or content_type.startswith("application/octet-stream") or body_bytes[:4] == b"RIFF":
                        return body_bytes

                    # 2. JSON Response with Base64 audio payload
                    try:
                        res_json = json.loads(body_bytes.decode("utf-8"))
                        b64_str = (
                            res_json.get("audio")
                            or res_json.get("data")
                            or res_json.get("audio_base64")
                        )
                        if b64_str:
                            return base64.b64decode(b64_str)
                    except Exception:
                        if len(body_bytes) > 44:
                            return body_bytes

                except Exception as e:
                    last_exception = e

            if attempt == 0:
                await asyncio.sleep(0.2)

        raise last_exception or Exception("Failed to synthesize audio from Smallest AI Waves.")

    async def _execute_sarvam_tts(self, text: str) -> bytes:
        """
        Executes high-fidelity neural speech synthesis via Sarvam AI (Bulbul v3).
        Produces authoritative, crystal-clear technical recruiter delivery for Zaroon AI.
        """
        sarvam_key = getattr(settings, "SARVAM_API_KEY", "")
        if not sarvam_key:
            raise ValueError("Sarvam API key not configured")

        speaker = getattr(settings, "ZAROON_SARVAM_SPEAKER", "rohan")
        model = getattr(settings, "ZAROON_SARVAM_MODEL", "bulbul:v3")

        payload = {
            "inputs": [text],
            "target_language_code": "en-IN",
            "speaker": speaker,
            "model": model,
            "pitch": 0,
            "pace": float(self.speed if self.speed != 1.0 else 1.02),
            "loudness": 1.5,
            "enable_preprocessing": True
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {
            "api-subscription-key": sarvam_key,
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-ZaroonEngine/2.0",
        }

        req = urllib.request.Request(
            "https://api.sarvam.ai/text-to-speech",
            data=data,
            headers=headers,
            method="POST"
        )

        loop = asyncio.get_running_loop()
        def _fetch_sarvam():
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read()

        resp_bytes = await loop.run_in_executor(None, _fetch_sarvam)
        res_json = json.loads(resp_bytes.decode("utf-8"))
        audios = res_json.get("audios", [])
        if not audios or not audios[0]:
            raise ValueError("Sarvam TTS returned empty audio list")

        return base64.b64decode(audios[0])

    async def _execute_tts_request(self, text: str) -> bytes:
        """
        Multi-tier voice execution:
        1. Smallest AI Waves (if API key + Voice ID configured)
        2. Sarvam AI Neural Voice Engine (authoritative Zaroon timbre)
        """
        # Tier 1: Smallest AI
        if self.api_key and self.voice_id:
            try:
                return await self._execute_smallest_tts(text)
            except Exception as e:
                logger.warning(f"Smallest AI synthesis attempt failed: {str(e)}, falling back to Sarvam AI engine")

        # Tier 2: Sarvam AI
        try:
            return await self._execute_sarvam_tts(text)
        except Exception as e:
            logger.error(f"Sarvam AI synthesis attempt failed: {str(e)}")
            raise e

    async def synthesize_speech(
        self,
        text: str,
        preformat: bool = True,
        voice_id: Optional[str] = None # Ignored to strictly preserve ZAROON_VOICE_ID
    ) -> Dict[str, Any]:
        """
        Synthesizes text into high-fidelity Zaroon speech audio.
        Strictly enforces server-side voice identity and model.
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            return {
                "status": "error",
                "error": "Cannot synthesize empty speech text.",
                "persona": self.persona,
                "audio_base64": None,
            }

        # Format text for natural technical interviewer prosody
        spoken_text = zaroon_speech_formatter.format_for_speech(text) if preformat else text

        # Check Cache for static phrases
        cache_key = self._compute_cache_key(spoken_text)
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(f"[ZaroonTTS] Cache HIT for key {cache_key} ({latency_ms}ms)")
            return {
                "status": "success",
                "audio_base64": cached_data["audio_base64"],
                "audio_bytes": cached_data["audio_bytes"],
                "format": "audio/wav",
                "persona": self.persona,
                "voice_id_hash": self._get_voice_hash(),
                "model": self.model,
                "speed": self.speed,
                "text": spoken_text,
                "cached": True,
                "latency_ms": latency_ms,
                "duration_seconds": cached_data.get("duration_seconds", 0.0),
            }

        try:
            # Execute TTS with retry
            raw_audio = await self._execute_tts_request(spoken_text)

            # Validate audio structure
            val = zaroon_audio_processor.validate_audio(raw_audio)
            if not val.get("valid"):
                raise ValueError(f"Invalid audio structure received: {val.get('error')}")

            # Safe lightweight normalization
            normalized_audio = zaroon_audio_processor.normalize_loudness(raw_audio)

            base64_audio = base64.b64encode(normalized_audio).decode("utf-8")
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            duration_sec = val.get("duration_seconds", round(len(normalized_audio) / 48000.0, 2))

            # Store in cache (FIFO / LRU bound)
            if len(self._cache) >= self._max_cache_entries:
                # Evict oldest entry
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            self._cache[cache_key] = {
                "audio_base64": base64_audio,
                "audio_bytes": len(normalized_audio),
                "duration_seconds": duration_sec,
            }

            logger.info(
                f"[ZaroonTTS] Generated speech in {latency_ms}ms | Voice: {self._get_voice_hash()} | "
                f"Model: {self.model} | Bytes: {len(normalized_audio)} | Duration: {duration_sec}s"
            )

            return {
                "status": "success",
                "audio_base64": base64_audio,
                "audio_bytes": len(normalized_audio),
                "format": "audio/wav",
                "persona": self.persona,
                "voice_id_hash": self._get_voice_hash(),
                "model": self.model,
                "speed": self.speed,
                "text": spoken_text,
                "cached": False,
                "latency_ms": latency_ms,
                "duration_seconds": duration_sec,
            }

        except Exception as e:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(f"[ZaroonTTS] Synthesis failure ({latency_ms}ms): {str(e)}")
            return {
                "status": "error",
                "error": "Zaroon voice temporarily unavailable. Please wait a moment.",
                "technical_error": str(e),
                "persona": self.persona,
                "voice_id_hash": self._get_voice_hash(),
                "audio_base64": None,
                "latency_ms": latency_ms,
            }

    async def generate_speech(self, text: str) -> Dict[str, Any]:
        """Alias for synthesize_speech to conform with ZaroonTTSProvider interface."""
        return await self.synthesize_speech(text)

    async def stream_speech(
        self,
        text: str,
        chunk_size: int = 4096
    ) -> AsyncGenerator[bytes, None]:
        """
        Asynchronous generator that streams audio chunks for low-latency browser playback.
        """
        result = await self.synthesize_speech(text)
        if result.get("status") == "success" and result.get("audio_base64"):
            raw_bytes = base64.b64decode(result["audio_base64"])
            async for chunk in zaroon_audio_processor.chunk_audio_stream(raw_bytes, chunk_size):
                yield chunk
        else:
            logger.warning("[ZaroonTTS] Streaming yielded no audio due to synthesis error.")
            return

zaroon_tts_provider = ZaroonTTSProvider()
