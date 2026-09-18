"""
Zavran AI — 100-Question Interview Preparation Router
Provides high-performance, fault-tolerant preparation of 100-question packs from
the Hugging Face HR Interview Dataset + internal verified generation layer.
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Header, Depends

from backend.models.interview_question import PrepareInterviewPackRequest, InterviewPack
from backend.services.question_retrieval import question_retrieval_engine
from backend.services.role_normalizer import RoleNormalizer
from backend.clerk_auth import ClerkAuth
from backend.workers.dataset_sync import dataset_sync_worker

logger = logging.getLogger("ZavranAI.API.Prepare")

prepare_router = APIRouter(prefix="/api", tags=["Interview Preparation & Dataset Integration"])


@prepare_router.post("/interview/prepare-pack", response_model=InterviewPack)
async def prepare_interview_pack_endpoint(
    req: PrepareInterviewPackRequest,
    authorization: Optional[str] = Header(None),
):
    """
    Prepares a balanced 100-question interview pack with verified dataset & generated provenance.
    Strictly enforces role relevance, deduplication, answer quality, and multi-level caching.
    """
    try:
        # Authenticate if header provided
        if authorization:
            auth_info = ClerkAuth.authenticate_request(authorization)
            if auth_info and not req.clerk_user_id:
                req.clerk_user_id = auth_info.get("user_id")

        pack = question_retrieval_engine.prepare_100_question_pack(
            target_role=req.target_role or "Full Stack AI Engineer",
            job_description=req.job_description or "",
            resume_text=req.resume_text or "",
            seniority=req.seniority or "Mid-Level",
            required_skills=req.required_skills or [],
            question_count=req.question_count or 100,
            interview_type=req.interview_type or "Technical",
        )
        return pack
    except Exception as e:
        logger.error(f"Error preparing 100-question pack: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to prepare interview pack: {str(e)}")


@prepare_router.post("/admin/dataset/sync")
async def trigger_dataset_sync_endpoint(
    limit: Optional[int] = 500,
    authorization: Optional[str] = Header(None),
):
    """
    Admin endpoint to trigger background synchronization from Hugging Face Dataset Server.
    """
    try:
        stats = await dataset_sync_worker.run_sync(limit=limit)
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Dataset sync error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@prepare_router.get("/admin/dataset/status")
async def get_dataset_sync_status(authorization: Optional[str] = Header(None)):
    """
    Returns current sync status and metrics for Hugging Face Ankshi dataset.
    """
    return {
        "dataset_name": dataset_sync_worker.ingestion_service.dataset_name,
        "circuit_breaker_state": dataset_sync_worker.ingestion_service.circuit_breaker.state,
        "last_sync_time": dataset_sync_worker.last_sync_time,
        "sync_stats": dataset_sync_worker.sync_stats,
    }
