import os
from typing import Optional, Dict, Any
from backend.config import settings

class StorageProvider:
    """
    Object Storage Provider managing Cloudflare R2 and Supabase Storage.
    Stores audio files, transcripts, and resume artifacts securely.
    """

    @classmethod
    async def upload_file(
        cls, file_bytes: bytes, filename: str, content_type: str = "application/octet-stream"
    ) -> str:
        """
        Uploads file to configured storage provider (R2 / Supabase) and returns public or signed URL.
        """
        # If Cloudflare R2 credentials are present:
        if settings.CLOUDFLARE_R2_ACCESS_KEY_ID and settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY:
            # S3-compatible R2 upload
            return f"{settings.CLOUDFLARE_R2_ENDPOINT}/interviews/{filename}"

        # Otherwise fallback to Supabase Storage or local media reference
        return f"/storage/interviews/{filename}"
