import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_zaroon_voice_endpoint():
    # 1. Test Zaroon dedicated test endpoint
    res = client.post("/api/voice/zaroon/test", json={"text": "Hello candidate, welcome."})
    assert res.status_code == 200
    data = res.json()
    assert data["persona"] == "zaroon"


def test_synthesize_voice_endpoint_zaroon():
    # 2. Test Synthesize endpoint for Zaroon
    res = client.post("/api/voice/synthesize", json={"text": "Let us discuss distributed systems.", "persona": "zaroon"})
    assert res.status_code == 200
    data = res.json()
    assert data["persona"] == "zaroon"


def test_synthesize_voice_endpoint_unauthorized():
    # 3. Test Synthesize endpoint for unauthorized persona
    res = client.post("/api/voice/synthesize", json={"text": "Candidate speaking", "persona": "candidate"})
    assert res.status_code == 400

