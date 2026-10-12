import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Header, Depends, Query
from pydantic import BaseModel
from backend.database import (
    get_user_by_email,
    get_user_by_id,
    create_or_update_user,
    authenticate_user,
    update_user_profile,
    save_interview,
    get_user_interviews,
    delete_interview
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
    date: Optional[str] = None
    time: Optional[str] = None
    candidate_name: Optional[str] = "Candidate"
    email: Optional[str] = None
    user_email: Optional[str] = None

@auth_router.post("/api/auth/register")
async def register(req: RegisterRequest):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    email_clean = req.email.strip().lower()
    existing = get_user_by_email(email_clean)
    
    # If user already exists with password, return user seamlessly or update name
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
    
    return {
        "success": True,
        "message": "Account created successfully",
        "user": user,
        "token": user["id"]
    }

@auth_router.post("/api/auth/login")
async def login(req: LoginRequest):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    email_clean = req.email.strip().lower()
    user = authenticate_user(email=email_clean, password=req.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "success": True,
        "message": "Authentication successful",
        "user": user,
        "token": user["id"]
    }

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
async def get_me(email: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = None
    if email:
        user = get_user_by_email(email.strip().lower())
    elif authorization:
        token = authorization.replace("Bearer ", "").strip()
        if token.startswith("usr_"):
            user = get_user_by_id(token)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "user": user
    }

@auth_router.post("/api/auth/profile")
async def update_profile(req: UpdateProfileRequest):
    if not req.email or not req.email.strip():
        raise HTTPException(status_code=400, detail="Email is required")
    
    user = update_user_profile(req.email.strip().lower(), req.dict(exclude_unset=True))
    return {
        "success": True,
        "message": "Profile updated successfully",
        "user": user
    }

@auth_router.get("/api/user/interviews")
async def list_interviews(email: Optional[str] = Query(None)):
    if not email:
        return {"success": True, "interviews": []}
    interviews = get_user_interviews(email.strip().lower())
    return {
        "success": True,
        "interviews": interviews
    }

@auth_router.post("/api/user/interviews/schedule")
async def schedule_interview_endpoint(req: ScheduleInterviewRequest):
    data = req.dict()
    data["user_email"] = (req.user_email or req.email or "").strip().lower()
    interview = save_interview(data)
    return {
        "success": True,
        "message": "Interview scheduled and stored in database",
        "interview": interview
    }

@auth_router.post("/api/user/interviews/{room_code}/status")
async def update_status_endpoint(room_code: str, req: Dict[str, Any]):
    status = req.get("status", "in_progress")
    score = req.get("score")
    email = req.get("email")
    updated = update_interview_status(room_code=room_code, status=status, score=score, email=email)
    return {
        "success": updated,
        "message": f"Interview status updated to {status}"
    }

@auth_router.post("/api/user/interviews/{room_code}/cancel")
async def cancel_interview_post(room_code: str, email: Optional[str] = Query(None)):
    updated = update_interview_status(room_code=room_code, status="cancelled", email=email)
    return {
        "success": updated,
        "message": "Interview marked as cancelled"
    }

@auth_router.delete("/api/user/interviews/{room_code}")
async def delete_interview_endpoint(room_code: str, email: Optional[str] = Query(None)):
    deleted = delete_interview(room_code, email)
    return {
        "success": deleted,
        "message": "Interview deleted" if deleted else "Interview not found"
    }
