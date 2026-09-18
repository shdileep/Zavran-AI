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
        is_configured = bool(self.api_key and self.voice_id)
        return {
            "valid": is_configured,
            "persona": self.persona,
            "model": self.model,
            "speed": self.speed,
            "sample_rate": self.sample_rate,
            "voice_configured": bool(self.voice_id),
            "voice_hash": self._get_voice_hash(),
            "api_key_configured": bool(self.api_key),
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Performs a non-invasive health check of the Zaroon TTS provider.
        """
        val = self.validate_voice()
        status = "healthy" if val["valid"] else "degraded"
        return {
            "status": status,
            "provider": "Smallest AI (Waves Lightning)",
            "persona": self.persona,
            "model": self.model,
            "speed": self.speed,
            "cached_entries": len(self._cache),
            "voice_id_configured": bool(self.voice_id),
        }

    async def _execute_tts_request(self, text: str) -> bytes:
        """
        Executes HTTP request to Smallest AI Waves TTS with retry and exponential backoff.
        """
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
                    # Use asyncio run_in_executor to avoid blocking the event loop
                    loop = asyncio.get_running_loop()
                    
                    def _fetch():
                        with urllib.request.urlopen(req, timeout=15) as resp:
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

                except urllib.error.HTTPError as e:
                    err_body = e.read().decode("utf-8", errors="ignore")
                    logger.warning(f"Smallest AI HTTP {e.code} on attempt {attempt+1} at {endpoint}: {err_body}")
                    last_exception = Exception(f"HTTP {e.code}: {err_body}")
                except Exception as e:
                    logger.warning(f"Smallest AI connection error on attempt {attempt+1} at {endpoint}: {str(e)}")
                    last_exception = e

            # Exponential backoff between attempts
            if attempt == 0:
                await asyncio.sleep(0.3)

        raise last_exception or Exception("Failed to synthesize audio from Smallest AI Waves.")

    async def synthesize_speech(
        self,
        text: str,
        preformat: bool = True,
        voice_id: Optional[str] = None # Ignored to strictly preserve ZAROON_VOICE_ID
    ) -> Dict[str, Any]:
        """
        Synthesizes text into high-fidelity Zaroon speech audio.
        Strictly enforces server-side voice ID and model.
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

        # Configuration check
        if not self.api_key:
            logger.error("Smallest AI API key (SMALLEST_API_KEY) is not configured.")
            return {
                "status": "error",
                "error": "Zaroon voice temporarily unavailable. Please wait a moment.",
                "technical_error": "Missing SMALLEST_API_KEY",
                "persona": self.persona,
                "audio_base64": None,
            }

        if not self.voice_id:
            logger.error("Zaroon Voice ID (ZAROON_VOICE_ID) is not configured.")
            return {
                "status": "error",
                "error": "Zaroon voice temporarily unavailable. Please wait a moment.",
                "technical_error": "Missing ZAROON_VOICE_ID. Please configure ZAROON_VOICE_ID in settings.",
                "persona": self.persona,
                "audio_base64": None,
            }

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

            # Store in cache if phrase is static or short common phrase
            if spoken_text in self.CACHEABLE_STATIC_PHRASES or len(spoken_text) < 30:
                if len(self._cache) < self._max_cache_entries:
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
