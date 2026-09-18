import os
import json
import logging
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException, Depends, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.config import settings, BASE_DIR
from backend.interview_engine import interview_engine, InterviewSession
from backend.clerk_auth import ClerkAuth
from backend.providers.tts_provider import get_tts_provider, ZaroonTTSProvider
from backend.providers.email_provider import EmailService
from backend.role_catalog import (
    get_all_roles,
    get_categories,
    get_roles_by_category,
    get_role_by_name,
    search_roles,
    get_total_role_count,
)
from backend.question_bank import question_bank
from backend.api.interview_prepare import prepare_router
from backend.api.zaroon_voice import zaroon_voice_router

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ZavranAI.API")

app = FastAPI(
    title="Zavran AI — Live Technical Interview Engine",
    description="Backend API and WebSocket Server for AI-Driven Live Technical Assessment",
    version="2.0.0",
)

app.include_router(prepare_router)
app.include_router(zaroon_voice_router)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# REST Request Models
# -----------------------------------------------------------------------------
class PrepareInterviewRequest(BaseModel):
    candidate_id: Optional[str] = None
    interview_id: Optional[str] = None
    candidate_name: Optional[str] = "Candidate"
    target_role: Optional[str] = "Full Stack AI Engineer"
    interviewer_name: Optional[str] = "Zaroon"
    org_name: Optional[str] = "Zavran AI Partner"
    resume_text: Optional[str] = ""
    jd_text: Optional[str] = ""
    job_description: Optional[str] = ""
    resume_id: Optional[str] = None
    seniority: Optional[str] = "Mid-Level"
    question_count: Optional[int] = 100
    clerk_user_id: Optional[str] = None

class SubmitAnswerRequest(BaseModel):
    answer_text: str

class ProcessResponseRequest(BaseModel):
    speech_text: Optional[str] = ""
    candidate_answer: Optional[str] = None
    question_id: Optional[str] = None
    question_index: Optional[int] = None
    duration_seconds: Optional[float] = 0.0
    role: Optional[str] = None
    interviewer: Optional[str] = None
    candidate_name: Optional[str] = None

class WelcomeEmailRequest(BaseModel):
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = None
    clerk_user_id: Optional[str] = None

class ScheduleEmailRequest(BaseModel):
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = None
    room_code: str
    role: str
    company: Optional[str] = None
    organization: Optional[str] = None
    interviewer_name: Optional[str] = "Zaroon"
    interview_date: Optional[str] = "Scheduled Date"
    interview_time: Optional[str] = "Scheduled Time"
    clerk_user_id: Optional[str] = None

class ReadyEmailRequest(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    interviewer_name: Optional[str] = None
    interview_date: Optional[str] = None
    interview_time: Optional[str] = None
    clerk_user_id: Optional[str] = None
    email: Optional[str] = None


class AuditSnapshotRequest(BaseModel):
    image_base64: str
    reason: str # "excessive_movement", "face_missing", "object_detected", "posture_change", "lighting_low"
    details: Optional[str] = ""

class ViolationRequest(BaseModel):
    event_type: str # "camera_off", "face_missing", "shoulder_framing_lost", "multiple_faces", "phone_detected", "tab_switch", "fullscreen_exit", "insufficient_lighting", etc.
    details: Optional[str] = ""
    confidence: Optional[float] = 1.0
    image_base64: Optional[str] = None
    candidate_id: Optional[str] = None
    category: Optional[str] = None

class ValidatePrecheckRequest(BaseModel):
    checks_passed: bool = True

class RecoveryRequest(BaseModel):
    recovered_type: str
    details: Optional[str] = ""

class ProtestViolationRequest(BaseModel):
    violation_id: Optional[str] = None
    reason: Optional[str] = "Candidate contested infraction"
    explanation: Optional[str] = ""
    candidate_id: Optional[str] = None

class CompleteInterviewRequest(BaseModel):
    clerk_user_id: Optional[str] = None
    reason: Optional[str] = "completed"

class VoiceTestRequest(BaseModel):
    text: str = "Hello. Welcome to your technical interview. Please introduce yourself."

class VoiceSynthesizeRequest(BaseModel):
    text: str
    persona: str = "zaroon"
    interview_id: Optional[str] = None

class AnalyzeJDRequest(BaseModel):
    jd_text: str

class GeneratePlanRequest(BaseModel):
    role: str
    job_description: Optional[str] = None
    seniority: Optional[str] = "Mid-Level"
    years_of_experience: Optional[str] = "3+"
    required_skills: Optional[List[str]] = None
    industry: Optional[str] = None
    duration_minutes: Optional[int] = 30
    difficulty: Optional[str] = "medium"
    candidate_name: Optional[str] = "Candidate"

class AdaptiveFollowupRequest(BaseModel):
    current_question: Dict[str, Any]
    candidate_answer: str
    session_history: Optional[List[Dict[str, Any]]] = None
    current_difficulty: Optional[str] = "medium"

class CreateQuestionRequest(BaseModel):
    role: str
    category: str
    skill: str
    question: str
    ideal_answer: str
    difficulty: Optional[str] = "medium"
    seniority: Optional[str] = "Mid-Level"
    industry: Optional[str] = ""
    job_description_context: Optional[str] = ""
    evaluation_criteria: Optional[List[str]] = []
    expected_concepts: Optional[List[str]] = []
    red_flags: Optional[List[str]] = []
    follow_up_questions: Optional[List[str]] = []
    estimated_time_seconds: Optional[int] = 90
    verified: Optional[bool] = True

class UpdateQuestionRequest(BaseModel):
    role: Optional[str] = None
    category: Optional[str] = None
    skill: Optional[str] = None
    question: Optional[str] = None
    ideal_answer: Optional[str] = None
    difficulty: Optional[str] = None
    seniority: Optional[str] = None
    industry: Optional[str] = None
    evaluation_criteria: Optional[List[str]] = None
    expected_concepts: Optional[List[str]] = None
    red_flags: Optional[List[str]] = None
    follow_up_questions: Optional[List[str]] = None
    verified: Optional[bool] = None

# -----------------------------------------------------------------------------
# Role Catalog Endpoints (200+ Roles)
# -----------------------------------------------------------------------------
@app.get("/api/roles")
async def list_roles(category: Optional[str] = None, q: Optional[str] = None, limit: int = 250):
    if q:
        roles = search_roles(q, limit=limit)
    elif category:
        roles = get_roles_by_category(category)
    else:
        roles = get_all_roles()
    return {
        "total_catalog_count": get_total_role_count(),
        "count": len(roles),
        "roles": roles[:limit]
    }

@app.get("/api/roles/categories")
async def list_role_categories():
    return {
        "categories": get_categories(),
        "total_roles": get_total_role_count()
    }

@app.get("/api/roles/{role_name}")
async def get_role_details(role_name: str):
    role = get_role_by_name(role_name)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found in catalog")
    return role

# -----------------------------------------------------------------------------
# Dynamic Question Generation & JD Endpoints
# -----------------------------------------------------------------------------
@app.post("/api/jd/analyze")
async def analyze_jd_endpoint(req: AnalyzeJDRequest):
    return await question_generator.analyze_job_description(req.jd_text)

@app.post("/api/questions/generate-plan")
async def generate_plan_endpoint(req: GeneratePlanRequest):
    plan = await question_generator.generate_interview_plan(
        role_name=req.role,
        job_description=req.job_description,
        seniority=req.seniority or "Mid-Level",
        years_of_experience=req.years_of_experience,
        required_skills=req.required_skills,
        industry=req.industry,
        duration_minutes=req.duration_minutes or 30,
        difficulty=req.difficulty or "medium",
        candidate_name=req.candidate_name or "Candidate"
    )
    return {
        "role": req.role,
        "total_questions": len(plan),
        "plan": plan
    }

@app.post("/api/questions/adaptive-followup")
async def adaptive_followup_endpoint(req: AdaptiveFollowupRequest):
    return await question_generator.evaluate_and_adapt_next(
        current_question=req.current_question,
        candidate_answer=req.candidate_answer,
        session_history=req.session_history,
        current_difficulty=req.current_difficulty or "medium"
    )

# -----------------------------------------------------------------------------
# Admin Question Bank Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/admin/questions")
async def admin_get_questions(
    role: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    seniority: Optional[str] = None,
    query: Optional[str] = None,
    verified_only: bool = False,
    limit: int = 100
):
    questions = question_bank.search_questions(
        role=role,
        category=category,
        difficulty=difficulty,
        seniority=seniority,
        query=query,
        verified_only=verified_only,
        limit=limit
    )
    return {
        "count": len(questions),
        "questions": questions
    }

@app.get("/api/admin/question-bank/stats")
async def admin_get_stats():
    return question_bank.get_stats()

@app.post("/api/admin/questions")
async def admin_create_question(req: CreateQuestionRequest):
    data = req.dict()
    saved = question_bank.save_question(data, reject_duplicates=True)
    return {"success": True, "question": saved}

@app.put("/api/admin/questions/{question_id}")
async def admin_update_question(question_id: str, req: UpdateQuestionRequest):
    data = {k: v for k, v in req.dict().items() if v is not None}
    updated = question_bank.update_question(question_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"success": True, "question": updated}

@app.delete("/api/admin/questions/{question_id}")
async def admin_delete_question(question_id: str):
    deleted = question_bank.delete_question(question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"success": True, "deleted_id": question_id}

@app.post("/api/admin/questions/{question_id}/verify")
async def admin_verify_question(question_id: str):
    verified = question_bank.verify_question(question_id, verified=True)
    if not verified:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"success": True, "verified_id": question_id}

# -----------------------------------------------------------------------------
# REST Endpoints (Existing Voice / Session / Integrity)
# -----------------------------------------------------------------------------
@app.post("/api/voice/zaroon/test")
async def test_zaroon_voice(req: VoiceTestRequest):
    """
    Dedicated test endpoint for Zaroon's exclusive cloned voice.
    Synthesizes speech using Smallest AI Waves and returns playable audio payload.
    """
    try:
        provider = ZaroonTTSProvider()
        result = await provider.synthesize_speech(text=req.text)
        if result.get("status") == "error":
            return {
                "success": False,
                "error": result.get("error", "Zaroon voice temporarily unavailable. Please wait a moment."),
                "persona": "zaroon",
                "audio_base64": None,
            }
        return {
            "success": True,
            "persona": "zaroon",
            "voice_id": result.get("voice_id") or result.get("voice_id_hash"),
            "voice_id_hash": result.get("voice_id_hash"),
            "format": result.get("format", "audio/wav"),
            "audio_base64": result.get("audio_base64"),
            "audio_bytes": result.get("audio_bytes"),
            "latency_ms": result.get("latency_ms"),
            "duration_seconds": result.get("duration_seconds"),
            "cached": result.get("cached", False),
        }
    except Exception as e:
        logger.error(f"Error testing Zaroon voice: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": "Zaroon voice temporarily unavailable. Please wait a moment.",
            "persona": "zaroon",
            "audio_base64": None,
        }

@app.post("/api/voice/synthesize")
async def synthesize_voice(req: VoiceSynthesizeRequest):
    """
    Exclusive Voice Routing Endpoint.
    Enforces that Zaroon uses ONLY the Smallest AI cloned voice ID,
    while Aarin and Soni use their respective existing voice engines.
    """
    try:
        provider = get_tts_provider(req.persona)
        result = await provider.synthesize_speech(text=req.text)
        if isinstance(result, dict) and result.get("status") == "error":
            return {
                "success": False,
                "error": result.get("error", "Voice synthesis temporarily unavailable."),
                "persona": req.persona,
                "audio_base64": None,
            }
        return {
            "success": True,
            "persona": req.persona,
            "format": result.get("format", "audio/wav"),
            "audio_base64": result.get("audio_base64"),
            "audio_url": result.get("audio_url"),
        }
    except ValueError as e:
        logger.warning(f"Voice routing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error synthesizing speech for {req.persona}: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"{req.persona.capitalize()} voice temporarily unavailable. Please wait a moment.",
            "persona": req.persona,
            "audio_base64": None,
        }
def verify_session_access(
    session: InterviewSession,
    authorization: Optional[str] = None,
    bind_if_unowned: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Strict server-side authorization check.
    If session is owned by a user_id, enforces that the incoming request has a valid token belonging to that exact user.
    If mismatch, raises 403 Forbidden.
    If unauthenticated and session has owner, raises 401 Unauthorized.
    """
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None

    if not session.clerk_user_id:
        if bind_if_unowned and auth_info and auth_info.get("user_id"):
            session.clerk_user_id = auth_info["user_id"]
            session.clerk_verified_email = auth_info.get("verified_email") or session.clerk_verified_email
            return auth_info
        if not auth_info or not auth_info.get("user_id"):
            raise HTTPException(
                status_code=401,
                detail="Authentication token required to access this interview session."
            )
        return auth_info

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication token required to access this interview session."
        )

    if not auth_info or not auth_info.get("user_id"):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token."
        )

    if auth_info["user_id"] != session.clerk_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: You do not own this interview resource."
        )

    return auth_info


class ScheduleInterviewRequest(BaseModel):
    room_code: Optional[str] = None
    role: str = "Full Stack AI Engineer"
    company: Optional[str] = "Zavran AI Partner"
    interviewer: Optional[str] = "Zaroon"
    interviewer_name: Optional[str] = "Zaroon"
    date: Optional[str] = "Today"
    time: Optional[str] = "Scheduled Time"
    candidate_name: Optional[str] = "Candidate"


class UserProfileRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    avatarUrl: Optional[str] = None
    resumeFileName: Optional[str] = None
    resumeMeta: Optional[str] = None
    isUploaded: Optional[bool] = False


class AdminEmailTestRequest(BaseModel):
    recipient_email: str
    candidate_name: Optional[str] = "Test Candidate"
    subject: Optional[str] = "Zavran AI — Admin Integration Verification"
    message: Optional[str] = "This is a verified test email from the Zavran AI secure delivery pipeline."


@app.get("/api/user/interviews")
async def get_user_interviews_endpoint(authorization: Optional[str] = Header(None)):
    """Returns ONLY the interviews belonging to the authenticated user."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    interviews = interview_engine.get_user_interviews(user_id)
    return {"success": True, "interviews": interviews}


@app.post("/api/user/interviews/schedule")
async def schedule_user_interview_endpoint(
    req: ScheduleInterviewRequest,
    authorization: Optional[str] = Header(None)
):
    """Schedules an interview strictly scoped to the authenticated user."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    email = auth_info.get("verified_email")
    created = interview_engine.schedule_user_interview(user_id, {
        "roomCode": req.room_code,
        "role": req.role,
        "company": req.company,
        "interviewer": req.interviewer,
        "interviewer_name": req.interviewer_name,
        "date": req.date,
        "time": req.time,
        "candidate_name": req.candidate_name or auth_info.get("name", "Candidate"),
    })
    
    session = interview_engine.sessions.get(created["roomCode"])
    if session and email:
        session.clerk_verified_email = email

    return {"success": True, "interview": created}


@app.post("/api/user/interviews/{interview_id}/cancel")
async def cancel_user_interview_endpoint(
    interview_id: str,
    authorization: Optional[str] = Header(None)
):
    """Cancels an interview strictly if owned by the authenticated user."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    cancelled = interview_engine.cancel_user_interview(user_id, interview_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Interview not found or unauthorized to cancel")
    return {"success": True, "cancelled_id": interview_id, "status": "cancelled"}


@app.delete("/api/user/interviews/{interview_id}")
async def delete_user_interview_endpoint(
    interview_id: str,
    authorization: Optional[str] = Header(None)
):
    """Deletes an interview strictly if owned by the authenticated user."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    deleted = interview_engine.delete_user_interview(user_id, interview_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Interview not found or unauthorized to delete")
    return {"success": True, "deleted_id": interview_id}


@app.get("/api/user/dashboard-stats")
async def get_user_dashboard_stats_endpoint(authorization: Optional[str] = Header(None)):
    """Computes authentic real-time dashboard analytics strictly for the authenticated user."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    stats = interview_engine.get_user_dashboard_stats(user_id)
    return {"success": True, "stats": stats}


@app.get("/api/user/export-csv")
async def export_user_interviews_csv_endpoint(authorization: Optional[str] = Header(None)):
    """Generates and streams a CSV export containing ONLY the authenticated user's real interviews."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    interviews = interview_engine.get_user_interviews(user_id)

    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Interview ID", "Role", "Company / Organization", "Interviewer",
        "Scheduled Date", "Scheduled Time", "Status", "Score / Accuracy", "Recommendation"
    ])
    for it in interviews:
        writer.writerow([
            it.get("roomCode") or it.get("id") or "",
            it.get("role") or "",
            it.get("company") or it.get("org") or "",
            it.get("interviewer") or it.get("interviewer_name") or "",
            it.get("date") or "",
            it.get("time") or "",
            it.get("status") or "scheduled",
            f"{it.get('score')}%" if it.get("score") is not None else "N/A",
            it.get("recommendation") or "N/A",
        ])

    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=zavran_interview_history_{user_id[:8]}.csv"
        }
    )


@app.get("/api/user/profile")
async def get_user_profile_endpoint(authorization: Optional[str] = Header(None)):
    """Fetches user profile strictly scoped to authenticated user ID."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    profile = interview_engine.get_user_profile(user_id)
    if not profile:
        profile = {
            "name": auth_info.get("name", "Candidate"),
            "email": auth_info.get("verified_email", ""),
            "role": "",
            "location": "",
            "phone": "",
            "avatarUrl": "",
            "resumeFileName": "",
            "resumeMeta": "",
            "isUploaded": False
        }
    return {"success": True, "profile": profile}


@app.post("/api/user/profile")
async def save_user_profile_endpoint(
    req: UserProfileRequest,
    authorization: Optional[str] = Header(None)
):
    """Saves user profile strictly scoped to authenticated user ID."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    profile_data = req.dict(exclude_unset=True)
    saved = interview_engine.save_user_profile(user_id, profile_data)
    return {"success": True, "profile": saved}


@app.get("/api/user/dossier")
async def get_user_dossier_endpoint(authorization: Optional[str] = Header(None)):
    """Fetches user resume dossier strictly scoped to authenticated user ID."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    dossier = interview_engine.get_user_dossier(user_id)
    return {"success": True, "dossier": dossier}


@app.post("/api/user/dossier")
async def save_user_dossier_endpoint(
    req: List[Dict[str, Any]],
    authorization: Optional[str] = Header(None)
):
    """Saves user resume dossier strictly scoped to authenticated user ID."""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    saved = interview_engine.save_user_dossier(user_id, req)
    return {"success": True, "dossier": saved}


@app.post("/api/admin/email/test")
async def admin_email_test_endpoint(
    req: AdminEmailTestRequest,
    authorization: Optional[str] = Header(None)
):
    """Protected admin test endpoint to verify email delivery without exposing keys."""
    auth_info = ClerkAuth.require_auth(authorization)
    recipient = (req.recipient_email or "").strip()
    if not recipient or "@" not in recipient:
        raise HTTPException(status_code=400, detail="Valid recipient email is required.")
    
    provider = EmailService.get_provider()
    provider_name = getattr(provider, "name", provider.__class__.__name__.replace("EmailProvider", "").lower())
    try:
        html = f"<h2>Admin Email Delivery Verification</h2><p>{req.message}</p><p>Sent by user: <code>{auth_info['user_id']}</code></p>"
        res = await provider.send_email(
            to_email=recipient,
            subject=req.subject or "Zavran AI — Admin Delivery Test",
            html_body=html,
            text_body=req.message or "Admin test email",
        )
        msg_id = res.get("id") or str(res.get("status_code", "200"))
        log_rec = interview_engine.log_email_event(
            recipient=recipient,
            template="ADMIN_TEST",
            provider=provider_name,
            status="ACCEPTED_BY_PROVIDER",
            user_id=auth_info["user_id"],
            provider_message_id=msg_id
        )
        return {
            "success": True,
            "provider": provider_name,
            "message_id": msg_id,
            "recipient": recipient,
            "status": "accepted",
            "log": log_rec,
        }
    except Exception as e:
        logger.error(f"Admin email test failed: {e}", exc_info=True)
        interview_engine.log_email_event(
            recipient=recipient,
            template="ADMIN_TEST",
            provider=provider_name,
            status="FAILED",
            user_id=auth_info["user_id"],
            failure_reason=str(e)
        )
        return {
            "success": False,
            "provider": provider_name,
            "error": str(e),
            "recipient": recipient
        }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Zavran AI Interview Engine",
        "llm_provider": settings.INTERVIEW_LLM_PROVIDER,
        "stt_provider": settings.STT_PROVIDER,
    }

@app.post("/api/interview/prepare")
async def prepare_interview(req: PrepareInterviewRequest, authorization: Optional[str] = Header(None)):
    """
    Ingests candidate resume and target JD, generates personalized question plan
    with private hidden rubrics, and creates active session state.
    """
    try:
        session = interview_engine.get_or_create_session(
            interview_id=req.interview_id,
            candidate_name=req.candidate_name or "Candidate",
            target_role=req.target_role or "Full Stack AI Engineer",
            interviewer_name=req.interviewer_name or "Zaroon",
            org_name=req.org_name or "Zavran AI Partner",
        )
        
        # Verify / Bind user identity
        auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
        if req.clerk_user_id:
            session.clerk_user_id = req.clerk_user_id
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(req.clerk_user_id)
            except Exception as ce:
                logger.warning(f"Could not pre-fetch Clerk email for {req.clerk_user_id}: {ce}")
        elif auth_info:
            session.clerk_user_id = auth_info.get("user_id")
            session.clerk_verified_email = auth_info.get("verified_email")

        effective_jd = req.jd_text or req.job_description or ""
        effective_resume = req.resume_text or ""
        safe_state = await interview_engine.prepare_interview_plan(
            session=session, resume_text=effective_resume, jd_text=effective_jd
        )
        return {"success": True, "session": safe_state}
    except Exception as e:
        logger.error(f"Error preparing interview: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interview/{interview_id}/session")
async def get_session(interview_id: str, authorization: Optional[str] = Header(None)):
    """Retrieves candidate-safe session state (strictly checks authorization)."""
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)
    return {"success": True, "session": session.get_candidate_safe_state()}

@app.post("/api/interview/{interview_id}/start")
async def start_interview(interview_id: str, authorization: Optional[str] = Header(None)):
    """Starts interview timer and sets session state to in_progress (checks auth)."""
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)
    safe_state = interview_engine.start_session(session)
    return {"success": True, "session": safe_state}

@app.post("/api/interview/{interview_id}/upload-audio")
async def upload_audio_answer(
    interview_id: str,
    file: UploadFile = File(...),
    fallback_text: Optional[str] = Form(""),
    authorization: Optional[str] = Header(None),
):
    """
    Accepts candidate audio recording, transcribes via AssemblyAI,
    evaluates against hidden criteria via LLM, and dispatches next action.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    try:
        audio_bytes = await file.read()
        res = await interview_engine.submit_answer(
            session=session, answer_text=fallback_text or "", audio_bytes=audio_bytes
        )
        return {"success": True, "data": res}
    except Exception as e:
        logger.error(f"Error processing audio answer: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/{interview_id}/submit-text-answer")
async def submit_text_answer(
    interview_id: str,
    req: SubmitAnswerRequest,
    authorization: Optional[str] = Header(None)
):
    """Fallback text submission endpoint with authorization check."""
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    try:
        res = await interview_engine.submit_answer(session=session, answer_text=req.answer_text)
        return {"success": True, "data": res}
    except Exception as e:
        logger.error(f"Error submitting text answer: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/welcome-email")
async def send_welcome_email_endpoint(
    req: WelcomeEmailRequest,
    authorization: Optional[str] = Header(None),
):
    """
    Sends the branded Zavran AI Welcome / Greeting email from support.zarvanai@gmail.com
    when a user signs up or newly logs into the candidate or enterprise portal.
    """
    recipient_email = (req.email or "").strip()
    candidate_name = (req.candidate_name or "Candidate").strip()

    if not recipient_email and req.clerk_user_id:
        try:
            recipient_email = ClerkAuth.get_verified_email(req.clerk_user_id) or ""
        except Exception as e:
            logger.warning(f"Could not fetch Clerk email for user {req.clerk_user_id}: {e}")

    if not recipient_email and authorization:
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            recipient_email = auth_info.get("verified_email") or ""
            if not req.candidate_name or req.candidate_name == "Candidate":
                candidate_name = auth_info.get("candidate_name") or candidate_name

    if not recipient_email or "@" not in recipient_email:
        raise HTTPException(status_code=400, detail="A valid recipient email is required to send the welcome email.")

    try:
        res = await EmailService.send_welcome_email(
            to_email=recipient_email,
            candidate_name=candidate_name,
        )
        return {
            "success": True,
            "message": f"Welcome greetings email sent to {recipient_email}.",
            "recipient_email": recipient_email,
            "provider_response": res,
        }
    except Exception as e:
        logger.error(f"Error sending welcome email: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

@app.post("/api/interview/schedule-email")
async def send_schedule_email_endpoint(
    req: ScheduleEmailRequest,
    authorization: Optional[str] = Header(None),
):
    """
    Sends the automated interview-scheduled confirmation email with all details:
    Role, Company, Interviewer, Date, Time, Room Code, and instructions.
    """
    session = interview_engine.get_or_create_session(
        interview_id=req.room_code,
        candidate_name=req.candidate_name or "Candidate",
        target_role=req.role,
        interviewer_name=req.interviewer_name or "Zaroon",
        org_name=req.organization or req.company or "Zavran AI Partner",
    )

    recipient_email = (req.email or "").strip()
    if req.clerk_user_id:
        session.clerk_user_id = req.clerk_user_id
        if not recipient_email:
            try:
                recipient_email = ClerkAuth.get_verified_email(req.clerk_user_id) or ""
            except Exception as e:
                logger.warning(f"Clerk email lookup: {e}")

    if not recipient_email and authorization:
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            session.clerk_user_id = auth_info.get("user_id")
            recipient_email = auth_info.get("verified_email") or ""

    if recipient_email:
        session.clerk_verified_email = recipient_email

    res = await interview_engine.send_interview_scheduled_email(
        session=session,
        company=req.company or req.organization or session.org_name,
        role=req.role or session.target_role,
        interviewer_name=req.interviewer_name or session.interviewer_name,
        interview_date=req.interview_date or "Scheduled Date",
        interview_time=req.interview_time or "Scheduled Time",
    )
    return {
        "success": res.get("success", False),
        "scheduled_email_sent": session.scheduled_email_sent,
        "recipient_email": session.clerk_verified_email,
        "detail": res.get("message") or res.get("error"),
    }

@app.post("/api/interview/{interview_id}/ready-email")
async def send_ready_email_endpoint(
    interview_id: str,
    req: Optional[ReadyEmailRequest] = None,
    authorization: Optional[str] = Header(None),
):
    """
    Automated Interview-Ready Email Dispatch Endpoint.
    Sends confirmation and room access link ~5 min before scheduled interview.
    Protected against duplicate sending (idempotent).
    """
    session = interview_engine.get_or_create_session(interview_id=interview_id)

    if req and req.email:
        session.clerk_verified_email = req.email.strip()

    if req and req.clerk_user_id:
        session.clerk_user_id = req.clerk_user_id
        if not session.clerk_verified_email:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(req.clerk_user_id)
            except Exception as e:
                logger.warning(f"Clerk email check: {e}")
    elif authorization:
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            session.clerk_user_id = auth_info.get("user_id")
            session.clerk_verified_email = auth_info.get("verified_email")

    res = await interview_engine.send_room_ready_email(
        session=session,
        company=req.company if req else session.org_name,
        role=req.role if req else session.target_role,
        organization=req.organization if req else session.org_name,
        interviewer_name=req.interviewer_name if req else session.interviewer_name,
        interview_date=req.interview_date if req else "Today",
        interview_time=req.interview_time if req else "Upcoming",
    )
    return {
        "success": res.get("success", False),
        "ready_email_sent": session.ready_email_sent,
        "recipient_email": session.clerk_verified_email,
        "detail": res.get("message") or res.get("error"),
    }

@app.post("/api/interview/{interview_id}/completed-email")
async def send_completed_email_endpoint(
    interview_id: str,
    authorization: Optional[str] = Header(None),
):
    """
    Manual/Immediate endpoint for dispatching the post-interview completion email.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]

    if authorization and not session.clerk_user_id:
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            session.clerk_user_id = auth_info.get("user_id")
            session.clerk_verified_email = auth_info.get("verified_email")

    res = await interview_engine._dispatch_completed_email(session)
    return {
        "success": res.get("success", False),
        "completed_email_sent": session.completed_email_sent,
        "recipient_email": session.clerk_verified_email,
        "detail": res.get("message") or res.get("error"),
    }

@app.post("/api/interview/{interview_id}/process-response")
async def process_response_endpoint(
    interview_id: str,
    req: ProcessResponseRequest,
    authorization: Optional[str] = Header(None)
):
    """
    1. Receives candidate spoken response in backend.
    2. Context-aware evaluation only up to where candidate stopped speaking.
    3. Summarizes answer internally in 1-2 seconds (never leaked to candidate UI).
    4. Generates short natural one-sentence acknowledgement/compliment.
    5. Selects/generates next question and returns sanitized state for automatic progression.
    6. Returns adaptive transition delay (2000ms for skip, 3000ms for normal completion).
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    speech = req.speech_text or req.candidate_answer or ""
    try:
        res = await interview_engine.process_candidate_response(
            session=session,
            speech_text=speech,
            duration_seconds=req.duration_seconds or 0.0
        )
        return {"success": True, "data": res}
    except Exception as e:
        logger.error(f"Error processing candidate response: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/{interview_id}/audit-snapshot")
async def audit_snapshot_endpoint(
    interview_id: str,
    req: AuditSnapshotRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Stores audit screenshot snapshot when face movement, framing loss, or object holding is detected.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    res = interview_engine.record_audit_snapshot(
        session=session,
        image_base64=req.image_base64,
        reason=req.reason,
        details=req.details or ""
    )
    return {"success": True, "data": res}

@app.post("/api/interview/{interview_id}/validate-precheck")
async def validate_precheck_endpoint(
    interview_id: str,
    req: ValidatePrecheckRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Validates on server that all mandatory pre-interview checks passed before room entry.
    """
    session = interview_engine.get_or_create_session(interview_id=interview_id)
    verify_session_access(session, authorization)
    res = interview_engine.validate_precheck(session, req.checks_passed)
    return {"success": True, "data": res}

@app.post("/api/interview/{interview_id}/violation")
async def record_integrity_violation(
    interview_id: str,
    req: ViolationRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Records integrity incidents (camera off, face missing, shoulder framing loss, phone, tab switch).
    Enforces authoritative 15-warning limit strictly on the backend.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    action_result = interview_engine.record_violation(
        session=session,
        event_type=req.event_type,
        details=req.details or "",
        confidence=req.confidence if req.confidence is not None else 1.0,
        evidence_base64=req.image_base64,
        candidate_id=req.candidate_id,
    )
    return {"success": True, "result": action_result}

@app.post("/api/interview/{interview_id}/recovery")
async def record_condition_recovery(
    interview_id: str,
    req: RecoveryRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Records dynamic recovery when a failing condition is restored (e.g. face detected again).
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    action_result = interview_engine.record_recovery(
        session=session,
        recovered_type=req.recovered_type,
        details=req.details or ""
    )
    return {"success": True, "result": action_result}

@app.post("/api/interview/{interview_id}/protest")
async def record_candidate_protest(
    interview_id: str,
    req: ProtestViolationRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Records candidate dispute/protest against a proctoring violation.
    Appends to audit trail and adjusts penalty if justified.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    action_result = interview_engine.protest_violation(
        session=session,
        violation_id=req.violation_id,
        reason=req.reason or "Candidate contested infraction",
        explanation=req.explanation or "",
        candidate_id=req.candidate_id,
    )
    return {"success": True, "result": action_result}

@app.post("/api/interview/{interview_id}/complete")
@app.post("/api/interview/{interview_id}/end")
async def complete_interview(
    interview_id: str,
    req: Optional[CompleteInterviewRequest] = None,
    authorization: Optional[str] = Header(None),
):
    """
    Handles candidate interview completion, binds Clerk authenticated identity if present,
    and initiates asynchronous post-interview evaluation and automated email report delivery.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    # Resolve Clerk identity if provided in payload or auth header
    if req and req.clerk_user_id:
        session.clerk_user_id = req.clerk_user_id
        if not session.clerk_verified_email:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(req.clerk_user_id)
            except Exception as ce:
                logger.warning(f"Could not retrieve Clerk email for {req.clerk_user_id}: {ce}")
    elif authorization:
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            session.clerk_user_id = auth_info.get("user_id")
            session.clerk_verified_email = auth_info.get("verified_email")

    reason = req.reason if req and req.reason else "completed"
    interview_engine.start_background_evaluation(session, reason=reason)

    return {
        "success": True,
        "message": "Interview completed. Your responses are now being evaluated across the complete interview. Your detailed feedback report will be sent to your registered email within approximately 10 minutes.",
        "status": session.evaluation_stage,
        "report_status": session.report_status,
        "progress": session.evaluation_progress,
        "stage_label": session.evaluation_stage_label,
        "session": session.get_candidate_safe_state(),
    }

@app.post("/api/interview/{interview_id}/retry-email")
async def retry_interview_email(
    interview_id: str,
    authorization: Optional[str] = Header(None),
):
    """
    Retries delivering the candidate evaluation report email without re-running the LLM evaluation.
    Requires that the report has already been generated.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    if not session.final_report:
        raise HTTPException(status_code=400, detail="Report has not been generated yet. Please wait for evaluation to complete.")

    result = await interview_engine.retry_email_delivery(session)
    return {
        "success": result.get("success", False),
        "report_status": session.report_status,
        "email_sent": session.email_sent,
        "emailed_at": session.emailed_at,
        "recipient_email": session.clerk_verified_email,
        "detail": result.get("message") or result.get("error"),
    }

@app.get("/api/interview/{interview_id}/report")
@app.get("/api/interview-report/{interview_id}")
async def get_interview_report(
    interview_id: str,
    authorization: Optional[str] = Header(None),
):
    """
    Retrieves final structured evaluation report or current async evaluation progress.
    Strict route: verifies candidate ownership and rejects unauthorized access with 403 Forbidden.
    Never exposes hidden rubrics, LLM prompts, or system API credentials.
    """
    if interview_id not in interview_engine.sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    session = interview_engine.sessions[interview_id]
    verify_session_access(session, authorization)

    if session.final_report:
        return {
            "success": True,
            "status": "ready",
            "report_status": session.report_status,
            "email_sent": session.email_sent,
            "emailed_at": session.emailed_at,
            "progress": 100,
            "stage_label": "Evaluation complete.",
            "report": session.final_report,
        }

    # If evaluation hasn't started yet, kick it off
    if not session.is_evaluating and session.evaluation_stage != "ready":
        interview_engine.start_background_evaluation(session, reason=session.completion_reason)

    return {
        "success": True,
        "status": "evaluating",
        "report_status": session.report_status,
        "email_sent": session.email_sent,
        "progress": session.evaluation_progress,
        "stage_label": session.evaluation_stage_label,
        "report": None,
    }


# -----------------------------------------------------------------------------
# WebSocket Live Duplex Protocol
# -----------------------------------------------------------------------------
@app.websocket("/ws/interview/{interview_id}")
async def interview_websocket(websocket: WebSocket, interview_id: str, token: Optional[str] = None):
    """
    Real-time duplex WebSocket connection for live questions, audio streaming,
    camera integrity alerts, and instant pause/resume synchronization.
    Authenticates candidate ownership to prevent stream hijacking.
    """
    if interview_id in interview_engine.sessions:
        session = interview_engine.sessions[interview_id]
        if session.clerk_user_id:
            auth_info = ClerkAuth.authenticate_request(f"Bearer {token}") if token else None
            if not auth_info or auth_info.get("user_id") != session.clerk_user_id:
                await websocket.close(code=1008)
                return
    else:
        session = interview_engine.get_or_create_session(interview_id=interview_id)

    await websocket.accept()
    session = interview_engine.get_or_create_session(interview_id=interview_id)

    try:
        # Initial greeting event
        await websocket.send_json({
            "event": "session_connected",
            "session": session.get_candidate_safe_state(),
        })

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            event_type = msg.get("event")

            if event_type == "start_interview":
                safe_state = interview_engine.start_session(session)
                await websocket.send_json({
                    "event": "interview_started",
                    "session": safe_state,
                })

            elif event_type in ["violation", "camera_warning", "record_violation"]:
                v_type = msg.get("violation_type") or msg.get("type") or "violation_warning"
                details = msg.get("details", "")
                confidence = float(msg.get("confidence", 1.0))
                image_b64 = msg.get("image_base64") or msg.get("image")
                candidate_id = msg.get("candidate_id")
                res = interview_engine.record_violation(
                    session=session,
                    event_type=v_type,
                    details=details,
                    confidence=confidence,
                    evidence_base64=image_b64,
                    candidate_id=candidate_id
                )
                if res.get("action") == "terminate":
                    await websocket.send_json({
                        "event": "interview_terminated",
                        "reason": res.get("message"),
                        "warning_count": res.get("warning_count", settings.MAX_VIOLATIONS),
                        "max_warnings": settings.MAX_VIOLATIONS,
                        "session": session.get_candidate_safe_state(),
                    })
                else:
                    await websocket.send_json({
                        "event": "violation_warning",
                        "action": res.get("action"),
                        "warning_count": res.get("warning_count"),
                        "max_warnings": settings.MAX_VIOLATIONS,
                        "violation": res.get("violation"),
                        "session": session.get_candidate_safe_state(),
                    })

            elif event_type in ["recovery", "camera_restored", "record_recovery"]:
                rec_type = msg.get("recovered_type") or msg.get("type") or "camera_restored"
                details = msg.get("details", "")
                res = interview_engine.record_recovery(session, recovered_type=rec_type, details=details)
                await websocket.send_json({
                    "event": "recovery_confirmed",
                    "recovered_type": rec_type,
                    "active_violations": res.get("active_violations", []),
                    "session": session.get_candidate_safe_state(),
                })

            elif event_type in ["protest", "protest_violation", "dispute_violation"]:
                v_id = msg.get("violation_id")
                reason = msg.get("reason", "Candidate contested infraction")
                explanation = msg.get("explanation", "")
                c_id = msg.get("candidate_id")
                res = interview_engine.protest_violation(
                    session=session,
                    violation_id=v_id,
                    reason=reason,
                    explanation=explanation,
                    candidate_id=c_id,
                )
                await websocket.send_json({
                    "event": "protest_recorded",
                    "protest": res.get("protest"),
                    "warning_count": res.get("warning_count"),
                    "total_protests": res.get("total_protests"),
                    "message": res.get("message"),
                    "session": session.get_candidate_safe_state(),
                })

            elif event_type == "submit_answer":
                ans_text = msg.get("text", "")
                result = await interview_engine.submit_answer(session, answer_text=ans_text)
                if result.get("is_finished"):
                    await websocket.send_json({
                        "event": "interview_completed",
                        "report": result.get("final_report"),
                    })
                else:
                    await websocket.send_json({
                        "event": "question_updated",
                        "interviewer_response": result.get("interviewer_response"),
                        "session": result.get("session_state"),
                    })

            elif event_type == "end_interview":
                res = await interview_engine.complete_session(session, reason="ended_by_candidate")
                await websocket.send_json({
                    "event": "interview_completed",
                    "report": res.get("final_report"),
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {interview_id}")
    except Exception as e:
        logger.error(f"WebSocket error in {interview_id}: {str(e)}", exc_info=True)


# -----------------------------------------------------------------------------
# Static Files / Frontend Mounting
# -----------------------------------------------------------------------------
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")

