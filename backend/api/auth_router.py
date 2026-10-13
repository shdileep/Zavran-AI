import logging
import time
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Header, Depends, Query, Response
from pydantic import BaseModel
from backend.clerk_auth import ClerkAuth
from backend.database import (
    get_user_by_email,
    get_user_by_id,
    create_or_update_user,
    authenticate_user,
    update_user_profile,
    save_interview,
    get_user_interviews,
    delete_interview,
    update_interview_status,
    delete_user_account_data,
    get_interview_by_room_code
)

logger = logging.getLogger("ZavranAI.AuthAPI")

auth_router = APIRouter(tags=["Authentication & Users"])

class RegisterRequest(BaseModel):
    email: str
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = "AI Engineer"
    auth_provider: Optional[str] = "local"
    phone: Optional[str] = None
    location: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None

class SyncUserRequest(BaseModel):
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_provider: Optional[str] = "clerk"
    clerk_user_id: Optional[str] = None

class UpdateProfileRequest(BaseModel):
    email: str
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None

class ScheduleInterviewRequest(BaseModel):
    room_code: Optional[str] = None
    role: Optional[str] = "Full Stack AI Engineer"
    company: Optional[str] = "Zavran AI Partner"
    interviewer: Optional[str] = "Zaroon"
    interviewer_name: Optional[str] = "Zaroon"
    date: Optional[str] = None
    time: Optional[str] = None
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = None
    user_email: Optional[str] = None
    scheduled_epoch: Optional[float] = None

class ConsentRequest(BaseModel):
    room_code: str
    camera_mic_consent: bool = True
    ai_evaluation_consent: bool = True
    retention_days: int = 90

@auth_router.post("/api/auth/register")
async def register(req: RegisterRequest, response: Response):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    email_clean = req.email.strip().lower()
    existing = get_user_by_email(email_clean)
    
    if existing and existing.get("password") and req.password:
        if existing["password"] != req.password.strip():
            raise HTTPException(status_code=400, detail="This email is already registered with a different password. Please sign in.")
    
    user = create_or_update_user(
        email=email_clean,
        name=req.name,
        password=req.password,
        auth_provider=req.auth_provider or "local",
        role=req.role or "AI Engineer",
        phone=req.phone,
        location=req.location
    )
    
    # Issue Secure HttpOnly session cookie
    response.set_cookie(
        key="zaveran_session",
        value=user["id"],
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=86400 * 7
    )
    
    return {
        "success": True,
        "message": "Account created successfully",
        "user": user,
        "token": user["id"]
    }

@auth_router.post("/api/auth/login")
async def login(req: LoginRequest, response: Response):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    email_clean = req.email.strip().lower()
    user = authenticate_user(email=email_clean, password=req.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Set HttpOnly session cookie
    response.set_cookie(
        key="zaveran_session",
        value=user["id"],
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=86400 * 7
    )
    
    return {
        "success": True,
        "message": "Authentication successful",
        "user": user,
        "token": user["id"]
    }

@auth_router.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="zaveran_session")
    return {"success": True, "message": "Logged out successfully"}

@auth_router.post("/api/auth/sync")
async def sync_user(req: SyncUserRequest):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    email_clean = req.email.strip().lower()
    user = create_or_update_user(
        email=email_clean,
        name=req.name,
        auth_provider=req.auth_provider or "clerk",
        avatar_url=req.avatar_url
    )
    
    return {
        "success": True,
        "user": user,
        "token": user["id"]
    }

@auth_router.get("/api/auth/me")
async def get_me(
    email: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    user = None
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        auth_info = ClerkAuth.authenticate_request(authorization)
        if auth_info:
            user = get_user_by_id(auth_info["user_id"]) or get_user_by_email(auth_info.get("verified_email", ""))
        elif token.startswith("usr_"):
            user = get_user_by_id(token)
    elif email:
        user = get_user_by_email(email.strip().lower())
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "user": user
    }

@auth_router.post("/api/auth/profile")
async def update_profile(req: UpdateProfileRequest, authorization: Optional[str] = Header(None)):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email is required")
        
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    if auth_info and auth_info.get("verified_email"):
        if auth_info["verified_email"].strip().lower() != req.email.strip().lower():
            raise HTTPException(status_code=403, detail="Forbidden: Cannot modify another user's profile")
            
    user = update_user_profile(req.email.strip().lower(), req.model_dump(exclude_unset=True))
    return {
        "success": True,
        "message": "Profile updated successfully",
        "user": user
    }

@auth_router.delete("/api/auth/account")
async def delete_account(
    authorization: Optional[str] = Header(None)
):
    """Enforces account deletion and GDPR data retention erasure"""
    auth_info = ClerkAuth.require_auth(authorization)
    user_id = auth_info["user_id"]
    email = auth_info.get("verified_email") or f"{user_id}@zaveran.ai"
    deleted = delete_user_account_data(user_id=user_id, email=email)
    return {"success": True, "message": "Account and all associated records permanently purged."}

@auth_router.get("/api/user/interviews")
async def list_interviews(
    email: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    """
    Returns ONLY the interviews belonging to the authenticated caller.
    If authorization header is provided, strictly isolates to that user.
    """
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    if auth_info:
        user_id = auth_info["user_id"]
        verified_email = auth_info.get("verified_email")
        # Query persistent database for this user
        interviews = get_user_interviews(user_id=user_id)
        if not interviews and verified_email:
            interviews = get_user_interviews(email=verified_email)
        return {"success": True, "interviews": interviews}

    if email:
        interviews = get_user_interviews(email=email.strip().lower())
        return {"success": True, "interviews": interviews}

    return {"success": True, "interviews": []}

@auth_router.post("/api/user/interviews/schedule")
async def schedule_interview_endpoint(
    req: ScheduleInterviewRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Schedules an interview, binding it immutably to the authenticated user ID and email.
    """
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    user_id = auth_info["user_id"] if auth_info else None
    user_email = (req.user_email or req.email or (auth_info.get("verified_email") if auth_info else "") or "").strip().lower()
    
    data = req.model_dump()
    data["user_id"] = user_id
    data["user_email"] = user_email
    data["candidate_name"] = req.candidate_name or (auth_info.get("name") if auth_info else "Candidate")
    
    interview = save_interview(data)
    
    # Also sync into in-memory engine if available
    from backend.interview_engine import interview_engine
    if user_id:
        interview_engine.schedule_user_interview(user_id, {
            "roomCode": interview["room_code"],
            "role": interview["role"],
            "company": interview["company"],
            "interviewer": interview["interviewer"],
            "date": interview["date"],
            "time": interview["time"],
            "candidate_name": interview["candidate_name"]
        })
        
    return {
        "success": True,
        "message": "Interview scheduled and persisted in database",
        "interview": interview
    }

@auth_router.post("/api/user/interviews/{room_code}/status")
async def update_status_endpoint(
    room_code: str,
    req: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    user_id = auth_info["user_id"] if auth_info else None
    
    # Ownership verification
    existing = get_interview_by_room_code(room_code)
    if existing and user_id and existing.get("user_id") and existing["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this interview")

    status = req.get("status", "in_progress")
    score = req.get("score")
    email = req.get("email") or (auth_info.get("verified_email") if auth_info else None)
    
    updated = update_interview_status(
        room_code=room_code,
        status=status,
        score=score,
        email=email,
        user_id=user_id
    )
    return {
        "success": updated,
        "message": f"Interview status updated to {status}"
    }

@auth_router.get("/api/user/interviews/{room_code}/status")
async def get_status_endpoint(
    room_code: str,
    authorization: Optional[str] = Header(None)
):
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    user_id = auth_info["user_id"] if auth_info else None
    
    existing = get_interview_by_room_code(room_code)
    if not existing:
        raise HTTPException(status_code=404, detail="Interview not found")
    if user_id and existing.get("user_id") and existing["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this interview")

    return {
        "success": True,
        "room_code": room_code,
        "status": existing.get("status", "scheduled"),
        "interview": existing
    }

@auth_router.post("/api/user/interviews/{room_code}/cancel")
async def cancel_interview_post(
    room_code: str,
    email: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    user_id = auth_info["user_id"] if auth_info else None
    
    existing = get_interview_by_room_code(room_code)
    if existing and user_id and existing.get("user_id") and existing["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this interview")

    updated = update_interview_status(
        room_code=room_code,
        status="cancelled",
        email=email,
        user_id=user_id
    )
    return {
        "success": updated,
        "message": "Interview marked as cancelled"
    }

@auth_router.delete("/api/user/interviews/{room_code}")
async def delete_interview_endpoint(
    room_code: str,
    email: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    auth_info = ClerkAuth.authenticate_request(authorization) if authorization else None
    user_id = auth_info["user_id"] if auth_info else None
    
    existing = get_interview_by_room_code(room_code)
    if existing and user_id and existing.get("user_id") and existing["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this interview")

    deleted = delete_interview(room_code, email=email, user_id=user_id)
    return {
        "success": deleted,
        "message": "Interview deleted" if deleted else "Interview not found"
    }
