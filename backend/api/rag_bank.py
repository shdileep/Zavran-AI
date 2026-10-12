"""
Zavran AI — Bank RAG API Router (PyMuPDF + T5 + Groq + Multi-Agent Engine)
Exposes sub-millisecond retrieval, resume extraction, and candidate interview question calibration.
"""

import time
import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header
from pydantic import BaseModel

from backend.services.bank_rag_engine import bank_rag_service, DocExtractorAgent
from backend.clerk_auth import ClerkAuth

logger = logging.getLogger("ZavranAI.API.BankRAG")

rag_router = APIRouter(prefix="/api/rag", tags=["Bank RAG & Candidate Question Calibration"])


class QueryBankRequest(BaseModel):
    query: str
    target_role: Optional[str] = None
    top_k: Optional[int] = 15


class CalibrateCandidateRequest(BaseModel):
    resume_text: str = ""
    target_role: str = "Full Stack AI Engineer"
    jd_text: Optional[str] = ""
    job_description: Optional[str] = ""
    seniority: Optional[str] = "Mid-Senior"
    question_count: Optional[int] = 20
    clerk_user_id: Optional[str] = None


@rag_router.get("/status")
async def get_rag_status():
    """Returns Bank RAG index health, ingested files, chunk count, and latency metrics."""
    try:
        chunks_count = len(bank_rag_service.indexer.chunks)
        matrix_shape = (
            bank_rag_service.indexer.embeddings_matrix.shape
            if bank_rag_service.indexer.embeddings_matrix is not None
            else [0, 0]
        )
        
        # Benchmark sub-millisecond latency
        sample_res = bank_rag_service.query("Kubernetes microservices architecture", target_role="DevOps Engineer", top_k=5)

        return {
            "status": "ready" if bank_rag_service.is_ready else "initializing",
            "indexed_documents": ["pdf1.pdf", "pdf2.pdf", "pdf3.pdf", "pdf4.pdf", "pdf5.docx", "HR PDF.pdf"],
            "total_chunks": chunks_count,
            "vector_dimension": matrix_shape[1] if len(matrix_shape) > 1 else 0,
            "benchmark_latency_ms": sample_res["latency_ms"],
            "groq_enabled": bank_rag_service.groq_agent.client is not None,
            "extractor": "PyMuPDF (fitz) + python-docx"
        }
    except Exception as e:
        logger.error(f"Error checking RAG status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/reindex")
async def trigger_reindex():
    """Forces re-indexing of all 5 Bank documents from scratch."""
    try:
        stats = bank_rag_service.reindex_bank_documents()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Re-indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/query")
async def query_bank_endpoint(req: QueryBankRequest):
    """Performs sub-millisecond vector similarity search across all 5 Bank documents."""
    try:
        res = bank_rag_service.query(
            query_text=req.query,
            target_role=req.target_role,
            top_k=req.top_k or 15
        )
        return res
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/upload-resume")
async def upload_candidate_resume(
    file: UploadFile = File(...)
):
    """
    Extracts text from candidate uploaded resume (PDF / DOCX / TXT) using PyMuPDF.
    Returns extracted text, detected skills, and metadata in milliseconds.
    """
    start_t = time.perf_counter()
    try:
        contents = await file.read()
        extracted_text = DocExtractorAgent.extract_candidate_resume(contents, file.filename)
        
        # Extract basic skills from resume
        from backend.services.skill_extractor import SkillExtractor
        extracted_skills = SkillExtractor.extract_skills_from_text(extracted_text)

        elapsed_ms = (time.perf_counter() - start_t) * 1000.0

        return {
            "success": True,
            "filename": file.filename,
            "size_kb": round(len(contents) / 1024.0, 1),
            "char_count": len(extracted_text),
            "extraction_latency_ms": round(elapsed_ms, 2),
            "extracted_text": extracted_text,
            "extracted_skills": extracted_skills
        }
    except Exception as e:
        logger.error(f"Resume upload & extraction error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")


@rag_router.post("/calibrate")
async def calibrate_candidate_endpoint(
    req: CalibrateCandidateRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Calibrates candidate's interview questions against Bank materials using PyMuPDF + T5 + Groq.
    """
    try:
        effective_jd = req.jd_text or req.job_description or ""
        calib = await bank_rag_service.calibrate_candidate(
            resume_text=req.resume_text or "",
            target_role=req.target_role or "Full Stack AI Engineer",
            jd_text=effective_jd,
            seniority=req.seniority or "Mid-Senior",
            question_count=req.question_count or 20
        )
        return {"success": True, **calib}
    except Exception as e:
        logger.error(f"Candidate calibration error: {e}")
        raise HTTPException(status_code=500, detail=f"Calibration error: {str(e)}")


class AutoMatchRequest(BaseModel):
    resume_text: str = ""
    role: str = "Full Stack AI Engineer"
    company: Optional[str] = ""
    role_count: Optional[int] = 25
    hr_count: Optional[int] = 3
    limit: Optional[int] = None
    include_hr: Optional[bool] = True


@rag_router.post("/auto-match")
async def auto_match_questions_endpoint(req: AutoMatchRequest):
    """
    Automatically activated when candidate uploads resume and chooses Company + Role.
    Scans the 22,677 Bank questions across all 6 documents and prepares:
    - 25 Role-based & Resume questions
    - 3 HR & Behavioral questions
    Total 28 questions with complete model answers in milliseconds (guaranteed < 1 minute).
    """
    try:
        res = bank_rag_service.auto_match(
            resume_text=req.resume_text or "",
            role=req.role or "Full Stack AI Engineer",
            company=req.company or "",
            role_count=req.role_count if req.role_count is not None else 25,
            hr_count=req.hr_count if req.hr_count is not None else 3,
            limit=req.limit,
            include_hr=req.include_hr if req.include_hr is not None else True
        )
        return res
    except Exception as e:
        logger.error(f"Auto-match error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.get("/search")
async def search_bank_endpoint(
    q: str = "",
    role: Optional[str] = None,
    category: Optional[str] = None,
    doc_name: Optional[str] = None,
    limit: Optional[int] = 20
):
    """
    Ultra-fast keystroke search across all 22,677 Bank questions and answers.
    """
    try:
        res = bank_rag_service.search(
            query=q,
            target_role=role,
            category=category,
            doc_name=doc_name,
            top_k=limit or 20
        )
        return res
    except Exception as e:
        logger.error(f"Search bank error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
