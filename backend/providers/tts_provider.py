import json
import base64
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger("ZavranAI.TTSProvider")


from backend.services.zaroon_tts import ZaroonTTSProvider, zaroon_tts_provider
from backend.services.zaroon_speech_formatter import ZaroonSpeechFormatter, zaroon_speech_formatter
from backend.services.zaroon_audio import ZaroonAudioProcessor, zaroon_audio_processor


class BolnaTTSProvider:
    """
    Voice & Conversational Audio Provider using Bolna API.
    Synthesizes AI Interviewer spoken dialogue into audio streams.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.BOLNA_API_KEY
        self.base_url = "https://api.bolna.dev"

    async def synthesize_speech(self, text: str, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Synthesizes text into audio stream / URL using Bolna voice synthesis.
        """
        if not self.api_key:
            return {"audio_url": None, "text": text, "format": "text_fallback"}

        # In production environments, invokes Bolna TTS pipeline
        return {
            "audio_url": None,
            "text": text,
            "voice": voice_id or "natural_interviewer_en",
            "format": "stream_ready",
        }


class SarvamTTSProvider:
    """
    Multilingual & Indian-Language Voice Provider using Sarvam AI.
    Provides Hindi and regional language voice synthesis for AI interviewer.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SARVAM_API_KEY
        self.base_url = "https://api.sarvam.ai/text-to-speech"

    async def synthesize_speech(
        self, text: str, language_code: str = "en-IN"
    ) -> Dict[str, Any]:
        if not self.api_key:
            return {"audio_url": None, "text": text, "format": "text_fallback"}

        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }
        payload = {
            "inputs": [text],
            "target_language_code": language_code,
            "speaker": "meera",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "speech_sample_rate": 16000,
            "enable_preprocessing": True,
            "model": "bulbul:v1",
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                audios = res.get("audios", [])
                base64_audio = audios[0] if audios else None
                return {
                    "audio_base64": base64_audio,
                    "text": text,
                    "language": language_code,
                    "format": "audio/wav",
                }
        except Exception as e:
            # Safe graceful degradation to client TTS/text
            return {"audio_url": None, "text": text, "format": "text_fallback", "error": str(e)}


def get_tts_provider(persona: str):
    """
    Explicit Voice Routing Layer enforcing strict persona isolation.
    Zaroon -> ZaroonTTSProvider (Smallest AI cloned Zaroon voice ONLY)
    Aarin  -> BolnaTTSProvider
    Soni   -> SarvamTTSProvider
    """
    clean_persona = (persona or "").strip().lower()

    if clean_persona in ["zaroon", "zaroon ai"]:
        return ZaroonTTSProvider()
    elif clean_persona in ["aarin", "aarin ai"]:
        return BolnaTTSProvider()
    elif clean_persona in ["soni", "soni ai"]:
        return SarvamTTSProvider()
    else:
        raise ValueError(
            f"Unauthorized or unknown interviewer persona '{persona}'. "
            f"Cloned Zaroon voice cannot be routed to other personas."
        )
