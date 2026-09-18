#!/usr/bin/env python3
"""
One-Time Administrative Setup Script: Zaroon Voice Cloning via Smallest AI
Reads source recording at D:\\Zevaran\\Zaroon.mp3, uploads to Smallest AI Voice Cloning API,
extracts the generated voice ID, and persists ZAROON_VOICE_ID in the .env configuration.
"""

import os
import sys
import json
import uuid
import urllib.request
import urllib.error
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.config import settings, load_env_file

AUDIO_SOURCE_PATH = BASE_DIR / "Zaroon.mp3"
ENV_PATH = BASE_DIR / ".env"


def encode_multipart_formdata(fields, files):
    """Encodes multipart/form-data for urllib without external dependencies."""
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    body = bytearray()

    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    for key, (filename, content, content_type) in files.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    content_type_header = f"multipart/form-data; boundary={boundary}"
    return content_type_header, bytes(body)


def update_env_variable(key: str, value: str, env_file: Path = ENV_PATH):
    """Safely updates or appends a key-value pair in .env file."""
    lines = []
    found = False
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith(f"{key}=") or stripped.startswith(f"{key} ="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)

    if not found:
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append(f"{key}={value}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"[SUCCESS] Updated {key}={value} in {env_file.name}")


def clone_zaroon_voice():
    print("=" * 70)
    print("ZAVRAN AI — ZAROON EXCLUSIVE VOICE CLONING (SMALLEST AI)")
    print("=" * 70)

    # 1. Verify Source Audio File
    if not AUDIO_SOURCE_PATH.exists():
        print(f"[ERROR] Authorized Zaroon audio source not found at: {AUDIO_SOURCE_PATH}")
        sys.exit(1)

    file_size_bytes = AUDIO_SOURCE_PATH.stat().st_size
    print(f"[OK] Source Recording Verified: {AUDIO_SOURCE_PATH.name} ({file_size_bytes} bytes / ~{file_size_bytes/1024:.1f} KB)")

    # 2. Verify API Key
    load_env_file()
    api_key = os.getenv("SMALLEST_API_KEY", "").strip()
    if not api_key:
        api_key = input("Enter your SMALLEST_API_KEY: ").strip()
        if not api_key:
            print("[ERROR] SMALLEST_API_KEY is required to proceed with voice cloning.")
            sys.exit(1)
        update_env_variable("SMALLEST_API_KEY", api_key)

    # Read audio bytes
    with open(AUDIO_SOURCE_PATH, "rb") as f:
        audio_bytes = f.read()

    print("[*] Initiating voice cloning request with Smallest AI Waves platform...")

    fields = {
        "displayName": "Zaroon",
        "name": "Zaroon AI",
        "language": "en",
        "accent": "en-US",
        "description": "Zaroon AI - Technical and Domain Rigor Evaluator",
    }
    files = {
        "file": (AUDIO_SOURCE_PATH.name, audio_bytes, "audio/mpeg"),
    }

    content_type_header, multipart_body = encode_multipart_formdata(fields, files)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type_header,
        "User-Agent": "ZavranAI-VoiceSetup/1.0",
    }

    endpoints = [
        "https://waves-api.smallest.ai/api/v1/voice-cloning",
        "https://api.smallest.ai/waves/v1/voice-cloning",
    ]

    cloned_voice_id = None
    response_data = None

    for endpoint in endpoints:
        try:
            print(f"[*] Contacting endpoint: {endpoint}...")
            req = urllib.request.Request(endpoint, data=multipart_body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_text = resp.read().decode("utf-8")
                response_data = json.loads(resp_text)
                
                # Extract voice ID from possible response formats
                cloned_voice_id = (
                    response_data.get("voice_id")
                    or response_data.get("voiceId")
                    or response_data.get("id")
                    or (response_data.get("data") if isinstance(response_data.get("data"), str) else None)
                    or (response_data.get("data", {}).get("voice_id") if isinstance(response_data.get("data"), dict) else None)
                    or (response_data.get("data", {}).get("voiceId") if isinstance(response_data.get("data"), dict) else None)
                )
                if cloned_voice_id:
                    print(f"[SUCCESS] Voice clone created successfully via {endpoint}!")
                    break
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            print(f"[WARN] Endpoint {endpoint} returned HTTP {e.code}: {err_msg}")
        except Exception as e:
            print(f"[WARN] Connection to {endpoint} failed: {str(e)}")

    if not cloned_voice_id:
        print("\n[ERROR] Failed to clone voice automatically via Smallest AI API.")
        if response_data:
            print(f"Provider Response: {response_data}")
        manual_id = input("\nIf you already created the voice ID in Smallest AI Console, enter it here (or press Enter to exit): ").strip()
        if manual_id:
            cloned_voice_id = manual_id
        else:
            sys.exit(1)

    # 3. Persist Voice ID
    print("\n" + "=" * 70)
    print(f"[OK] EXCLUSIVE ZAROON VOICE ID: {cloned_voice_id}")
    print("=" * 70)
    update_env_variable("ZAROON_VOICE_ID", cloned_voice_id)

    print("\n[SETUP COMPLETE] Zaroon voice ID is now persisted and ready for production interviews.")
    print("Start the backend server to use Zaroon with his exclusive cloned voice.")


if __name__ == "__main__":
    clone_zaroon_voice()