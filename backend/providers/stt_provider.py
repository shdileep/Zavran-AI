import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from backend.config import settings

class AssemblyAISTTProvider:
    """
    Dedicated Speech-to-Text (STT) Provider using AssemblyAI API.
    Converts candidate audio recordings into clean text transcripts with confidence metadata.
    Does NOT perform answer evaluation or scoring.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ASSEMBLYAI_API_KEY
        self.upload_url = "https://api.assemblyai.com/v2/upload"
        self.transcript_url = "https://api.assemblyai.com/v2/transcript"

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY is not configured in .env")
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }

    async def transcribe_audio_bytes(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Uploads audio buffer to AssemblyAI, triggers transcription job, and polls until complete.
        Returns:
        {
          "transcript": str,
          "confidence": float,
          "audio_duration": float,
          "words_count": int,
          "status": "completed"
        }
        """
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY is not configured")

        # Step 1: Upload audio file buffer
        upload_req = urllib.request.Request(
            self.upload_url,
            data=audio_data,
            headers={"authorization": self.api_key, "content-type": "application/octet-stream"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(upload_req, timeout=30) as resp:
                upload_res = json.loads(resp.read().decode("utf-8"))
                audio_url = upload_res.get("upload_url")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"AssemblyAI audio upload failed ({e.code}): {e.read().decode('utf-8')}")

        # Step 2: Request transcription
        transcript_payload = {
            "audio_url": audio_url,
            "punctuate": True,
            "format_text": True,
            "speech_model": "nano", # Fast response for live interviews
        }
        req = urllib.request.Request(
            self.transcript_url,
            data=json.dumps(transcript_payload).encode("utf-8"),
            headers=self._get_headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                job_res = json.loads(resp.read().decode("utf-8"))
                transcript_id = job_res.get("id")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"AssemblyAI transcript request failed ({e.code}): {e.read().decode('utf-8')}")

        # Step 3: Poll for transcription completion (max 25s)
        polling_url = f"{self.transcript_url}/{transcript_id}"
        poll_req = urllib.request.Request(polling_url, headers=self._get_headers(), method="GET")

        for _ in range(25):
            time.sleep(1.0)
            try:
                with urllib.request.urlopen(poll_req, timeout=15) as resp:
                    status_res = json.loads(resp.read().decode("utf-8"))
                    status = status_res.get("status")
                    if status == "completed":
                        return {
                            "transcript": status_res.get("text", "").strip(),
                            "confidence": status_res.get("confidence", 1.0),
                            "audio_duration": status_res.get("audio_duration", 0.0),
                            "words_count": len(status_res.get("words", [])),
                            "audio_url": audio_url,
                            "status": "completed",
                        }
                    elif status == "error":
                        raise RuntimeError(f"AssemblyAI transcription error: {status_res.get('error')}")
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"AssemblyAI polling error ({e.code})")

        raise TimeoutError("AssemblyAI transcription timed out")
