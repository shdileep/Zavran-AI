import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.services.zaroon_tts import zaroon_tts_provider, ZaroonTTSProvider
from backend.services.zaroon_speech_formatter import zaroon_speech_formatter
from backend.services.zaroon_audio import zaroon_audio_processor
from backend.config import settings

logger = logging.getLogger("ZavranAI.ZaroonVoiceAPI")

zaroon_voice_router = APIRouter(
    prefix="/api/voice/zaroon",
    tags=["Zaroon Voice Engine"]
)


class ZaroonSynthesizeRequest(BaseModel):
    text: str
    interview_id: Optional[str] = None
    preformat: Optional[bool] = True


class ZaroonStreamRequest(BaseModel):
    text: str
    interview_id: Optional[str] = None


class ZaroonFormatRequest(BaseModel):
    text: str


@zaroon_voice_router.post("/synthesize")
async def synthesize_zaroon_speech(req: ZaroonSynthesizeRequest):
    """
    Dedicated speech synthesis endpoint for Zaroon AI.
    Strictly uses the configured cloned Zaroon voice ID (ZAROON_VOICE_ID) and Lightning v3.1 model.
    Rejects any voice override from client requests.
    """
    try:
        result = await zaroon_tts_provider.synthesize_speech(
            text=req.text,
            preformat=req.preformat if req.preformat is not None else True
        )
        if result.get("status") == "error":
            return {
                "success": False,
                "error": result.get("error", "Zaroon voice temporarily unavailable. Please wait a moment."),
                "persona": "zaroon",
                "audio_base64": None,
                "latency_ms": result.get("latency_ms", 0.0),
            }

        return {
            "success": True,
            "persona": "zaroon",
            "format": result.get("format", "audio/wav"),
            "audio_base64": result.get("audio_base64"),
            "audio_bytes": result.get("audio_bytes"),
            "duration_seconds": result.get("duration_seconds"),
            "latency_ms": result.get("latency_ms"),
            "cached": result.get("cached", False),
            "voice_id_hash": result.get("voice_id_hash"),
            "text": result.get("text"),
        }
    except Exception as e:
        logger.error(f"Zaroon voice synthesis exception: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": "Zaroon voice temporarily unavailable. Please wait a moment.",
            "persona": "zaroon",
            "audio_base64": None,
        }


@zaroon_voice_router.post("/stream")
async def stream_zaroon_speech(req: ZaroonStreamRequest):
    """
    Ultra-low latency chunked audio streaming endpoint for live candidate interaction.
    Streams raw audio bytes as they are synthesized to minimize Time-To-First-Audio (TTFT).
    """
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Cannot stream empty text.")

    formatted_text = zaroon_speech_formatter.format_for_speech(req.text)
    
    return StreamingResponse(
        zaroon_tts_provider.stream_speech(formatted_text),
        media_type="audio/wav",
        headers={
            "X-Persona": "zaroon",
            "X-Model": zaroon_tts_provider.model,
            "Cache-Control": "no-cache",
        }
    )


@zaroon_voice_router.post("/format")
async def format_interviewer_text(req: ZaroonFormatRequest):
    """
    Inspects how raw text is formatted for natural conversational technical prosody.
    """
    formatted = zaroon_speech_formatter.format_for_speech(req.text)
    return {
        "success": True,
        "original_text": req.text,
        "formatted_text": formatted,
    }


@zaroon_voice_router.get("/health")
async def zaroon_voice_health():
    """
    Non-invasive health status of Zaroon Production Voice Engine.
    """
    return zaroon_tts_provider.health_check()


@zaroon_voice_router.post("/validate")
async def validate_zaroon_voice():
    """
    Validates server-side Zaroon voice configuration.
    """
    return zaroon_tts_provider.validate_voice()
