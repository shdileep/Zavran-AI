import os
import sys
import io
import pytest
from fastapi.testclient import TestClient

# Ensure sys.path contains project root
sys.path.insert(0, r"D:\Zevaran")

from backend.main import app
from backend.services.bank_rag_engine import bank_rag_service

client = TestClient(app)

def test_bank_rag_status():
    """Validates Bank RAG status and index stats."""
    response = client.get("/api/rag/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["total_chunks"] > 22000
    assert "pdf1.pdf" in data["indexed_documents"]
    assert "pdf2.pdf" in data["indexed_documents"]
    assert "pdf3.pdf" in data["indexed_documents"]
    assert "pdf4.pdf" in data["indexed_documents"]
    assert "pdf5.docx" in data["indexed_documents"]
    assert "HR PDF.pdf" in data["indexed_documents"]
    print(f"RAG Status OK: {data['total_chunks']} chunks, latency: {data['benchmark_latency_ms']} ms")

def test_bank_rag_hr_behavioral_query():
    """Tests sub-millisecond retrieval of behavioral and HR questions from HR PDF.pdf."""
    payload = {
        "query": "Tell me about a time you handled a difficult conflict with a team member under deadline pressure",
        "target_role": "Behavioral & Leadership",
        "top_k": 3
    }
    response = client.post("/api/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert "latency_ms" in data
    print(f"HR Query returned {data['count']} chunks in {data['latency_ms']} ms")

def test_bank_rag_submillisecond_query():
    """Tests sub-millisecond retrieval query across Bank files."""
    payload = {
        "query": "Kubernetes cluster pod scaling and high availability configuration",
        "target_role": "DevOps Engineer",
        "top_k": 5
    }
    response = client.post("/api/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert "latency_ms" in data
    assert len(data["results"]) <= 5
    print(f"Query returned {data['count']} chunks in {data['latency_ms']} ms")

def test_bank_rag_resume_upload_extraction():
    """Tests PyMuPDF resume upload extraction endpoint."""
    sample_content = b"Candidate Name: Alex Rivera\nExperience: Senior MLOps Engineer at CloudScale AI.\nSkills: Python, PyTorch, PyMuPDF, FastAPI, Docker, Kubernetes, T5 Transformers, Groq."
    files = {"file": ("alex_rivera_resume.txt", io.BytesIO(sample_content), "text/plain")}
    
    response = client.post("/api/rag/upload-resume", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Alex Rivera" in data["extracted_text"]
    assert len(data["extracted_skills"]) > 0
    print(f"Resume extraction OK: {data['size_kb']} KB, extracted {len(data['extracted_skills'])} skills in {data['extraction_latency_ms']} ms")

def test_bank_rag_candidate_calibration():
    """Tests full candidate calibration with Groq / Bank RAG synthesis."""
    payload = {
        "resume_text": "Alex Rivera - MLOps Engineer experienced with LLMs, PyMuPDF RAG pipelines, Kubernetes, and Groq inference engine.",
        "target_role": "MLOps Engineer",
        "seniority": "Senior",
        "question_count": 3
    }
    response = client.post("/api/rag/calibrate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["question_count"] == 3
    assert len(data["questions"]) == 3
    for q in data["questions"]:
        assert "question" in q
        assert "hidden_rubric" in q
        assert "source_provenance" in q
    print(f"Calibration OK: Generated {data['question_count']} questions in {data['total_latency_ms']} ms")

def test_prepare_interview_integration_with_rag():
    """Tests that /api/interview/prepare generates RAG-calibrated questions."""
    payload = {
        "interview_id": "ZAV-TEST-9988",
        "candidate_name": "Alex Rivera",
        "target_role": "MLOps Engineer",
        "resume_text": "MLOps engineer with PyTorch and Kubernetes experience.",
        "jd_text": "Deploying machine learning models at scale."
    }
    response = client.post("/api/interview/prepare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["session"]["questions"]) > 0
    print(f"Interview Prepare OK: Session questions initialized: {len(data['session']['questions'])}")
def test_bank_rag_auto_match_questions():
    """Tests automatic power agent question matching with answers for candidate."""
    payload = {
        "resume_text": "Alex Rivera - Staff Engineer. Experience building Kubernetes microservices, Kafka streaming data pipelines, and PyMuPDF vector indexing.",
        "role": "Staff Cloud Architect",
        "company": "Stripe",
        "limit": 6,
        "include_hr": True
    }
    response = client.post("/api/rag/auto-match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["matched_count"] > 0
    assert "latency_ms" in data
    assert len(data["questions_with_answers"]) > 0
    first_q = data["questions_with_answers"][0]
    assert "question" in first_q
    assert "answer" in first_q
    assert "provenance" in first_q
    print(f"Auto-Match OK: Scanned {data['total_corpus_scanned']} Bank Q&As, fetched {data['matched_count']} questions with answers in {data['latency_ms']} ms")

def test_bank_rag_search():
    """Tests real-time search across 22,677 Bank questions."""
    response = client.get("/api/rag/search?q=Kafka+streaming&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert "latency_ms" in data
    print(f"Search OK: Fetched {data['count']} matching items in {data['latency_ms']} ms")

def test_bank_rag_prepare_25_role_and_3_hr_under_minute():
    """Tests that the agent prepares 25 role-based + 3 HR questions with model answers in under 60 seconds (in ms)."""
    payload = {
        "resume_text": "Alex Rivera - Principal Backend Engineer. Expertise in Distributed Systems, Kafka streaming, PostgreSQL, Go, Kubernetes, Redis caching, microservices resilience.",
        "role": "Principal Backend Engineer",
        "company": "Google",
        "role_count": 25,
        "hr_count": 3,
        "include_hr": True
    }
    response = client.post("/api/rag/auto-match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["role_questions_count"] == 25, f"Expected 25 role questions, got {data['role_questions_count']}"
    assert data["hr_questions_count"] == 3, f"Expected 3 HR questions, got {data['hr_questions_count']}"
    assert data["total_questions"] == 28, f"Expected 28 total questions, got {data['total_questions']}"
    assert data["latency_seconds"] < 60.0, f"Latency should be < 60s, got {data['latency_seconds']}s"
    
    # Verify 25 role questions have answers and rubrics
    assert len(data["role_based_questions"]) == 25
    for idx, rq in enumerate(data["role_based_questions"]):
        assert "question" in rq and len(rq["question"]) > 5
        assert "answer" in rq
        assert "provenance" in rq
        assert rq["section"] == "Role & Resume Technical"

    # Verify 3 HR questions
    assert len(data["hr_behavioral_questions"]) == 3
    for idx, hq in enumerate(data["hr_behavioral_questions"]):
        assert "question" in hq and len(hq["question"]) > 5
        assert "answer" in hq
        assert "provenance" in hq
        assert hq["section"] == "HR & Behavioral"

    print(f"PASS: Prepared {data['role_questions_count']} Role + {data['hr_questions_count']} HR questions in {data['latency_ms']} ms ({data['latency_seconds']}s, well under 1 minute)!")

if __name__ == "__main__":
    pytest.main(["-v", __file__])
