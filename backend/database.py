import os
import json
import time
import uuid
import sqlite3
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

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
    
    # 1. Users table with permanent user id, email, authentication identity, profile & resume facts
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
    
    # 2. Interviews table with scheduling timestamps, owner user_id, room_code, and report publication timer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id TEXT PRIMARY KEY,
        room_code TEXT UNIQUE NOT NULL,
        user_id TEXT,
        user_email TEXT NOT NULL,
        candidate_name TEXT NOT NULL,
        role TEXT NOT NULL,
        company TEXT NOT NULL,
        interviewer TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT DEFAULT 'Scheduled',
        score REAL,
        scheduled_epoch REAL,
        completed_epoch REAL,
        report_available_epoch REAL,
        created_at TEXT
    )
    """)

    # 3. Resume facts table (structured skills, experience, claims)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_facts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        email TEXT NOT NULL,
        skills TEXT,
        experience_summary TEXT,
        projects TEXT,
        extracted_facts_json TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # 4. Interview plans & question banks prepared asynchronously before interview
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_plans (
        id TEXT PRIMARY KEY,
        interview_id TEXT UNIQUE NOT NULL,
        target_role TEXT NOT NULL,
        plan_json TEXT NOT NULL,
        prepared_at TEXT,
        FOREIGN KEY (interview_id) REFERENCES interviews(room_code)
    )
    """)

    # 5. Question and answer pairs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_qa_pairs (
        id TEXT PRIMARY KEY,
        interview_id TEXT NOT NULL,
        question_index INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        question_text TEXT NOT NULL,
        topic TEXT,
        reference_concepts TEXT,
        candidate_answer TEXT,
        concepts_demonstrated TEXT,
        concepts_missing TEXT,
        score REAL,
        scoring_rationale TEXT,
        answered_at REAL,
        FOREIGN KEY (interview_id) REFERENCES interviews(room_code)
    )
    """)

    # 6. Monitoring events & evidence metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoring_events (
        id TEXT PRIMARY KEY,
        interview_id TEXT NOT NULL,
        candidate_id TEXT NOT NULL,
        signal_type TEXT NOT NULL,
        confidence REAL NOT NULL,
        severity TEXT,
        inconclusive INTEGER DEFAULT 0,
        has_evidence INTEGER DEFAULT 0,
        evidence_uri TEXT,
        details TEXT,
        created_at REAL,
        FOREIGN KEY (interview_id) REFERENCES interviews(room_code)
    )
    """)

    # 7. Monitoring consent & privacy preferences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoring_consents (
        id TEXT PRIMARY KEY,
        interview_id TEXT UNIQUE NOT NULL,
        candidate_id TEXT NOT NULL,
        camera_mic_consent INTEGER DEFAULT 1,
        ai_evaluation_consent INTEGER DEFAULT 1,
        retention_days INTEGER DEFAULT 90,
        consented_at REAL,
        FOREIGN KEY (interview_id) REFERENCES interviews(room_code)
    )
    """)

    # 8. Final reports
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_reports (
        id TEXT PRIMARY KEY,
        interview_id TEXT UNIQUE NOT NULL,
        candidate_id TEXT NOT NULL,
        overall_score REAL NOT NULL,
        status TEXT NOT NULL,
        completed_at REAL NOT NULL,
        published_at REAL,
        available_at REAL NOT NULL,
        report_json TEXT NOT NULL,
        FOREIGN KEY (interview_id) REFERENCES interviews(room_code)
    )
    """)

    # 9. Account deletion / data retention requests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS privacy_requests (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        email TEXT NOT NULL,
        request_type TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        requested_at REAL
    )
    """)

    # Run lightweight column migrations if older tables exist
    cursor.execute("PRAGMA table_info(interviews)")
    columns = [col[1] for col in cursor.fetchall()]
    if "user_id" not in columns:
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN user_id TEXT")
        except Exception:
            pass
    if "scheduled_epoch" not in columns:
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN scheduled_epoch REAL")
        except Exception:
            pass
    if "completed_epoch" not in columns:
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN completed_epoch REAL")
        except Exception:
            pass
    if "report_available_epoch" not in columns:
        try:
            cursor.execute("ALTER TABLE interviews ADD COLUMN report_available_epoch REAL")
        except Exception:
            pass

    conn.commit()
    conn.close()
    logger.info(f"Permanent SQLite user database initialized at {DB_PATH}")

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
    resume_text: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    if not email:
        raise ValueError("Email is required")
    
    email_clean = email.strip().lower()
    existing = get_user_by_email(email_clean)
    now = datetime.now(timezone.utc).isoformat()
    
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
        if not user_id:
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
        if password:
            return create_or_update_user(email=email_clean, password=password, auth_provider="local")
        return None
    
    if user.get("password") and password:
        if user["password"] != password.strip():
            return None
    
    now = datetime.now(timezone.utc).isoformat()
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

def save_interview(interview: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    data = dict(interview or {})
    data.update(kwargs)
    room_code = data.get("room_code") or data.get("roomCode") or data.get("id")
    if not room_code:
        room_code = f"ZAV-{str(uuid.uuid4())[:8].upper()}"
    
    user_id = data.get("user_id") or ""
    user_email = (data.get("user_email") or data.get("email") or "").strip().lower()
    interview = data
    
    # Associate user_id from database if available
    if not user_id and user_email:
        u = get_user_by_email(user_email)
        if u:
            user_id = u["id"]
    elif user_id and not user_email:
        u = get_user_by_id(user_id)
        if u:
            user_email = u["email"]

    candidate_name = interview.get("candidate_name") or interview.get("name") or "Candidate"
    role = interview.get("role") or "Full Stack AI Engineer"
    company = interview.get("company") or interview.get("organization") or "Zavran AI Partner"
    interviewer = interview.get("interviewer") or "Zaroon"
    date_val = interview.get("date") or datetime.now(timezone.utc).strftime("%B %d, %Y")
    time_val = interview.get("time") or interview.get("timeSlot") or "10:00 AM"
    status = interview.get("status") or "Scheduled"
    score = interview.get("score")
    now = datetime.now(timezone.utc).isoformat()
    scheduled_epoch = interview.get("scheduled_epoch") or interview.get("scheduledAt") or time.time()
    completed_epoch = interview.get("completed_epoch")
    report_available_epoch = interview.get("report_available_epoch")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT OR REPLACE INTO interviews (
        id, room_code, user_id, user_email, candidate_name, role, company,
        interviewer, date, time, status, score, scheduled_epoch, completed_epoch, report_available_epoch, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        room_code, room_code, user_id, user_email, candidate_name, role, company,
        interviewer, date_val, time_val, status, score, scheduled_epoch, completed_epoch, report_available_epoch, now
    ))
    
    conn.commit()
    conn.close()
    
    return {
        "id": room_code,
        "roomCode": room_code,
        "room_code": room_code,
        "user_id": user_id,
        "user_email": user_email,
        "candidate_name": candidate_name,
        "role": role,
        "company": company,
        "interviewer": interviewer,
        "date": date_val,
        "time": time_val,
        "timeSlot": time_val,
        "status": status,
        "score": score,
        "scheduled_epoch": scheduled_epoch,
        "completed_epoch": completed_epoch,
        "report_available_epoch": report_available_epoch
    }

def get_user_interviews(email: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    if user_id:
        cursor.execute("SELECT * FROM interviews WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    elif email:
        email_clean = email.strip().lower()
        cursor.execute("SELECT * FROM interviews WHERE LOWER(user_email) = ? ORDER BY created_at DESC", (email_clean,))
    else:
        conn.close()
        return []
        
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        d["roomCode"] = d["room_code"]
        d["timeSlot"] = d["time"]
        results.append(d)
    return results

def get_interview_by_room_code(room_code: str) -> Optional[Dict[str, Any]]:
    if not room_code:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interviews WHERE room_code = ?", (room_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["roomCode"] = d["room_code"]
        d["timeSlot"] = d["time"]
        return d
    return None

def update_interview_status(
    room_code: str,
    status: str,
    score: Optional[float] = None,
    email: Optional[str] = None,
    user_id: Optional[str] = None,
    completed_epoch: Optional[float] = None,
    report_available_epoch: Optional[float] = None
) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = ["status = ?"]
    params = [status]
    
    if score is not None:
        updates.append("score = ?")
        params.append(score)
    if completed_epoch is not None:
        updates.append("completed_epoch = ?")
        params.append(completed_epoch)
    if report_available_epoch is not None:
        updates.append("report_available_epoch = ?")
        params.append(report_available_epoch)
        
    where = ["room_code = ?"]
    params.append(room_code)
    
    if user_id:
        where.append("user_id = ?")
        params.append(user_id)
    elif email:
        where.append("LOWER(user_email) = ?")
        params.append(email.strip().lower())
        
    sql = f"UPDATE interviews SET {', '.join(updates)} WHERE {' AND '.join(where)}"
    cursor.execute(sql, tuple(params))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_interview(room_code: str, email: Optional[str] = None, user_id: Optional[str] = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("DELETE FROM interviews WHERE room_code = ? AND user_id = ?", (room_code, user_id))
    elif email:
        email_clean = email.strip().lower()
        cursor.execute("DELETE FROM interviews WHERE room_code = ? AND LOWER(user_email) = ?", (room_code, email_clean))
    else:
        cursor.execute("DELETE FROM interviews WHERE room_code = ?", (room_code,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def save_interview_report(
    interview_id: str,
    candidate_id: str = "",
    report: Optional[Dict[str, Any]] = None,
    overall_score: float = 80.0,
    status: str = "completed",
    completed_at: float = 0.0,
    available_at: float = 0.0,
    **kwargs
) -> Dict[str, Any]:
    import json
    rep_dict = dict(report or {})
    rep_dict.update(kwargs)
    if not completed_at:
        completed_at = time.time()
    if not available_at:
        available_at = completed_at + 600.0
    conn = get_connection()
    cursor = conn.cursor()
    report_id = f"rep_{uuid.uuid4().hex[:10]}"
    cursor.execute("""
    INSERT OR REPLACE INTO interview_reports (
        id, interview_id, candidate_id, overall_score, status, completed_at, available_at, report_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id, interview_id, candidate_id, overall_score, status, completed_at, available_at, json.dumps(rep_dict)
    ))
    conn.commit()
    conn.close()
    return {"id": report_id, "available_at": available_at}

def get_interview_report(interview_id: str) -> Optional[Dict[str, Any]]:
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interview_reports WHERE interview_id = ?", (interview_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("report_json"):
        try:
            d["report"] = json.loads(d["report_json"])
        except Exception:
            d["report"] = None
    return d

def delete_user_account_data(user_id: str, email: str) -> bool:
    """Full GDPR / Privacy data deletion across all tables for user"""
    conn = get_connection()
    cursor = conn.cursor()
    email_clean = email.strip().lower()
    
    cursor.execute("DELETE FROM monitoring_events WHERE candidate_id = ? OR interview_id IN (SELECT room_code FROM interviews WHERE user_id = ? OR LOWER(user_email) = ?)", (user_id, user_id, email_clean))
    cursor.execute("DELETE FROM monitoring_consents WHERE candidate_id = ? OR interview_id IN (SELECT room_code FROM interviews WHERE user_id = ? OR LOWER(user_email) = ?)", (user_id, user_id, email_clean))
    cursor.execute("DELETE FROM interview_reports WHERE candidate_id = ? OR interview_id IN (SELECT room_code FROM interviews WHERE user_id = ? OR LOWER(user_email) = ?)", (user_id, user_id, email_clean))
    cursor.execute("DELETE FROM interview_qa_pairs WHERE interview_id IN (SELECT room_code FROM interviews WHERE user_id = ? OR LOWER(user_email) = ?)", (user_id, email_clean))
    cursor.execute("DELETE FROM resume_facts WHERE user_id = ? OR LOWER(email) = ?", (user_id, email_clean))
    cursor.execute("DELETE FROM interviews WHERE user_id = ? OR LOWER(user_email) = ?", (user_id, email_clean))
    cursor.execute("DELETE FROM users WHERE id = ? OR LOWER(email) = ?", (user_id, email_clean))
    
    conn.commit()
    conn.close()
    return True

def save_user_profile(
    user_id: str,
    email: str,
    name: str = "",
    target_role: str = "",
    skills: Optional[List[str]] = None,
    experience_years: int = 0
) -> Dict[str, Any]:
    skills_json = json.dumps(skills or [])
    u = create_or_update_user(
        email=email,
        name=name,
        role=target_role,
        user_id=user_id
    )
    # Also save resume facts if skills provided
    conn = get_connection()
    cursor = conn.cursor()
    rf_id = f"rf_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT OR REPLACE INTO resume_facts (
        id, user_id, email, skills, experience_summary, created_at
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (rf_id, user_id, email.lower(), skills_json, f"{experience_years} years experience", now))
    conn.commit()
    conn.close()
    return u

def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    u = get_user_by_id(user_id)
    if not u:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume_facts WHERE user_id = ?", (user_id,))
    rf = cursor.fetchone()
    conn.close()
    profile = {
        "id": u["id"],
        "email": u["email"],
        "name": u["name"],
        "target_role": u.get("role", ""),
        "skills": []
    }
    if rf and rf["skills"]:
        try:
            profile["skills"] = json.loads(rf["skills"])
        except Exception:
            profile["skills"] = []
    return profile

def save_qa_pair(
    interview_id: str,
    question_id: str,
    question_text: str,
    answer_text: str,
    score: float = 0.0,
    feedback: str = "",
    question_index: int = 0
) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    pair_id = f"qa_{uuid.uuid4().hex[:8]}"
    now_epoch = time.time()
    cursor.execute("""
    INSERT INTO interview_qa_pairs (
        id, interview_id, question_index, question_id, question_text,
        candidate_answer, answered_at, score, scoring_rationale
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pair_id, interview_id, question_index, question_id, question_text,
        answer_text, now_epoch, score, feedback
    ))
    conn.commit()
    conn.close()
    return pair_id

def get_qa_pairs(interview_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interview_qa_pairs WHERE interview_id = ? ORDER BY question_index ASC", (interview_id,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["answer_text"] = d.get("candidate_answer")
        results.append(d)
    return results

def record_monitoring_consent(interview_id: str, user_id: str, consent_version: str = "1.0") -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    c_id = f"mc_{uuid.uuid4().hex[:8]}"
    now = time.time()
    cursor.execute("""
    INSERT OR REPLACE INTO monitoring_consents (
        id, interview_id, candidate_id, camera_mic_consent, ai_evaluation_consent, consented_at
    ) VALUES (?, ?, ?, 1, 1, ?)
    """, (c_id, interview_id, user_id, now))
    conn.commit()
    conn.close()
    return True

def has_monitoring_consent(interview_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM monitoring_consents WHERE interview_id = ?", (interview_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None
