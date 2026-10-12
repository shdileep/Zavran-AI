import os
import sqlite3
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger("ZavranAI.Database")

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "users.db")

os.makedirs(DB_DIR, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table with UNIQUE lowercase email constraint to prevent duplicates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password TEXT,
        auth_provider TEXT DEFAULT 'local',
        role TEXT DEFAULT 'AI Engineer',
        phone TEXT DEFAULT '',
        location TEXT DEFAULT '',
        avatar_url TEXT DEFAULT '',
        resume_file_name TEXT DEFAULT '',
        resume_text TEXT DEFAULT '',
        created_at TEXT,
        last_login TEXT
    )
    """)
    
    # Interviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id TEXT PRIMARY KEY,
        room_code TEXT UNIQUE NOT NULL,
        user_email TEXT NOT NULL,
        candidate_name TEXT NOT NULL,
        role TEXT NOT NULL,
        company TEXT NOT NULL,
        interviewer TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT DEFAULT 'Scheduled',
        score REAL,
        created_at TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    logger.info(f"SQLite user database initialized at {DB_PATH}")

# Initialize on import
init_db()

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    if not email:
        return None
    email_clean = email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email_clean,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    if not user_id:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def create_or_update_user(
    email: str,
    name: Optional[str] = None,
    password: Optional[str] = None,
    auth_provider: str = "local",
    role: Optional[str] = None,
    phone: Optional[str] = None,
    location: Optional[str] = None,
    avatar_url: Optional[str] = None,
    resume_file_name: Optional[str] = None,
    resume_text: Optional[str] = None
) -> Dict[str, Any]:
    if not email:
        raise ValueError("Email is required")
    
    email_clean = email.strip().lower()
    existing = get_user_by_email(email_clean)
    now = datetime.utcnow().isoformat()
    
    # Format a clean fallback display name if missing
    if not name or name.strip() == "" or name.lower() == "candidate" or name.startswith("usr_"):
        prefix = email_clean.split("@")[0].replace(".", " ").replace("_", " ")
        name = " ".join([word.capitalize() for word in prefix.split()])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if existing:
        # Update existing user without losing data
        user_id = existing["id"]
        new_name = name or existing["name"]
        new_pwd = password if password else existing["password"]
        new_prov = auth_provider or existing["auth_provider"]
        new_role = role or existing.get("role") or "AI Engineer"
        new_phone = phone if phone is not None else existing.get("phone", "")
        new_loc = location if location is not None else existing.get("location", "")
        new_avatar = avatar_url if avatar_url is not None else existing.get("avatar_url", "")
        new_resume_name = resume_file_name if resume_file_name is not None else existing.get("resume_file_name", "")
        new_resume_text = resume_text if resume_text is not None else existing.get("resume_text", "")
        
        cursor.execute("""
        UPDATE users SET 
            name = ?,
            password = ?,
            auth_provider = ?,
            role = ?,
            phone = ?,
            location = ?,
            avatar_url = ?,
            resume_file_name = ?,
            resume_text = ?,
            last_login = ?
        WHERE id = ?
        """, (
            new_name, new_pwd, new_prov, new_role, new_phone, new_loc,
            new_avatar, new_resume_name, new_resume_text, now, user_id
        ))
    else:
        # Create new unique user
        import base64
        user_id = "usr_" + base64.b64encode(email_clean.encode()).decode().replace("=", "")
        cursor.execute("""
        INSERT INTO users (
            id, email, name, password, auth_provider, role, phone, location,
            avatar_url, resume_file_name, resume_text, created_at, last_login
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, email_clean, name, password or "", auth_provider,
            role or "AI Engineer", phone or "", location or "",
            avatar_url or "", resume_file_name or "", resume_text or "",
            now, now
        ))
    
    conn.commit()
    conn.close()
    
    return get_user_by_email(email_clean)

def authenticate_user(email: str, password: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if not email:
        return None
    email_clean = email.strip().lower()
    user = get_user_by_email(email_clean)
    
    if not user:
        # If user does not exist yet and valid password is provided, auto-create seamlessly
        if password:
            return create_or_update_user(email=email_clean, password=password, auth_provider="local")
        return None
    
    # If user has a password, check it
    if user.get("password") and password:
        if user["password"] != password.strip():
            return None
    
    # Update last login
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user["id"]))
    conn.commit()
    conn.close()
    
    return get_user_by_email(email_clean)

def update_user_profile(email: str, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    email_clean = email.strip().lower()
    user = get_user_by_email(email_clean)
    if not user:
        # Create user with profile data
        return create_or_update_user(
            email=email_clean,
            name=profile_data.get("name"),
            role=profile_data.get("role"),
            phone=profile_data.get("phone"),
            location=profile_data.get("location"),
            avatar_url=profile_data.get("avatar_url")
        )
    
    conn = get_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    
    allowed = ["name", "role", "phone", "location", "avatar_url", "resume_file_name", "resume_text", "password"]
    for k in allowed:
        if k in profile_data:
            fields.append(f"{k} = ?")
            values.append(profile_data[k])
    
    if not fields:
        conn.close()
        return user
    
    values.append(user["id"])
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    
    return get_user_by_email(email_clean)

def save_interview(interview: Dict[str, Any]) -> Dict[str, Any]:
    room_code = interview.get("room_code") or interview.get("roomCode") or interview.get("id")
    if not room_code:
        import uuid
        room_code = f"ZAV-{str(uuid.uuid4())[:8].upper()}"
    
    user_email = (interview.get("user_email") or interview.get("email") or "").strip().lower()
    candidate_name = interview.get("candidate_name") or interview.get("name") or "Candidate"
    role = interview.get("role") or "Full Stack AI Engineer"
    company = interview.get("company") or interview.get("organization") or "Zavran AI Partner"
    interviewer = interview.get("interviewer") or "Zaroon"
    date_val = interview.get("date") or datetime.utcnow().strftime("%B %d, %Y")
    time_val = interview.get("time") or interview.get("timeSlot") or "10:00 AM"
    status = interview.get("status") or "Scheduled"
    score = interview.get("score")
    now = datetime.utcnow().isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT OR REPLACE INTO interviews (
        id, room_code, user_email, candidate_name, role, company,
        interviewer, date, time, status, score, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        room_code, room_code, user_email, candidate_name, role, company,
        interviewer, date_val, time_val, status, score, now
    ))
    
    conn.commit()
    conn.close()
    
    return {
        "id": room_code,
        "roomCode": room_code,
        "room_code": room_code,
        "user_email": user_email,
        "candidate_name": candidate_name,
        "role": role,
        "company": company,
        "interviewer": interviewer,
        "date": date_val,
        "time": time_val,
        "timeSlot": time_val,
        "status": status,
        "score": score
    }

def get_user_interviews(email: str) -> List[Dict[str, Any]]:
    if not email:
        return []
    email_clean = email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interviews WHERE LOWER(user_email) = ? ORDER BY created_at DESC", (email_clean,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        d["roomCode"] = d["room_code"]
        d["timeSlot"] = d["time"]
        results.append(d)
    return results

def update_interview_status(room_code: str, status: str, score: Optional[float] = None, email: Optional[str] = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    if score is not None:
        if email:
            cursor.execute("UPDATE interviews SET status = ?, score = ? WHERE room_code = ? AND LOWER(user_email) = ?", (status, score, room_code, email.strip().lower()))
        else:
            cursor.execute("UPDATE interviews SET status = ?, score = ? WHERE room_code = ?", (status, score, room_code))
    else:
        if email:
            cursor.execute("UPDATE interviews SET status = ? WHERE room_code = ? AND LOWER(user_email) = ?", (status, room_code, email.strip().lower()))
        else:
            cursor.execute("UPDATE interviews SET status = ? WHERE room_code = ?", (status, room_code))
            
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_interview(room_code: str, email: Optional[str] = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    if email:
        email_clean = email.strip().lower()
        cursor.execute("DELETE FROM interviews WHERE room_code = ? AND LOWER(user_email) = ?", (room_code, email_clean))
    else:
        cursor.execute("DELETE FROM interviews WHERE room_code = ?", (room_code,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
