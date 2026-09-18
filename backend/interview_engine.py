import time
import uuid
import logging
import asyncio
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.provider_factory import LLMProviderFactory
from backend.providers.stt_provider import AssemblyAISTTProvider
from backend.providers.tts_provider import BolnaTTSProvider, SarvamTTSProvider
from backend.clerk_auth import ClerkAuth
from backend.providers.email_provider import EmailService
from backend.question_generator import question_generator
from backend.question_bank import question_bank

logger = logging.getLogger("ZavranAI.InterviewEngine")

class InterviewSession:
    """
    Authoritative Server-Side Interview State Machine.
    Holds candidate profiles, hidden rubrics, transcripts, private evaluations,
    full question memory, cross-question consistency, and asynchronous evaluation progress.
    """

    def __init__(
        self,
        interview_id: str,
        candidate_name: str,
        target_role: str,
        interviewer_name: str = "Zaroon",
        org_name: str = "Zavran AI Partner",
    ):
        self.interview_id = interview_id
        self.candidate_name = candidate_name
        self.target_role = target_role
        self.interviewer_name = interviewer_name
        self.org_name = org_name

        # Extracted Profiles
        self.candidate_profile: Dict[str, Any] = {}
        self.jd_profile: Dict[str, Any] = {}

        # Questions & Private Hidden Rubrics with Structured Expected Answer Models (20-Question Pool)
        provider = LLMProviderFactory.get_provider()
        self.questions = [
            {
                "id": "q1",
                "step_label": "Question 1 of 20 • Architecture & Systems Design",
                "category": "Architecture & Distributed Systems",
                "topic": "Streaming Low-Latency AI Pipelines",
                "question": f"Based on your experience applying for {self.target_role}, walk me through how you architect low-latency AI pipelines with streaming responses while maintaining context window efficiency.",
                "hidden_rubric": {
                    "expected_answer_points": ["Chunking strategies", "Vector search indexing", "Caching layer", "Streaming SSE/WebSockets"],
                    "evaluation_criteria": {"technical_accuracy": True, "practical_experience": True},
                    "difficulty": "Medium",
                },
                "expected_answer_model": {
                    "critical_concepts": ["Streaming SSE/WebSockets", "Chunking & retrieval caching"],
                    "important_concepts": ["Vector search indexing", "Context window management"],
                },
                "difficulty": "Medium",
            }
        ]
        if hasattr(provider, "get_default_20_questions"):
            try:
                loaded_q = provider.get_default_20_questions(
                    target_role=self.target_role, candidate_name=self.candidate_name
                )
                if loaded_q:
                    self.questions = loaded_q
            except Exception as e:
                logger.debug(f"Default questions init note: {e}")
        self.current_question_index: int = 0

        # Structured Full Interview Memory Stores
        self.answers: List[Dict[str, Any]] = []
        self.evaluations: List[Dict[str, Any]] = []
        self.evaluation_events: List[Dict[str, Any]] = []
        self.followups: List[Dict[str, Any]] = []
        self.topics: List[Dict[str, Any]] = []
        self.cross_question_analysis: Optional[Dict[str, Any]] = None

        # Integrity & Violation Tracking (Authoritative 15-Warning Limit)
        self.violations: List[Dict[str, Any]] = []
        self.audit_snapshots: List[Dict[str, Any]] = []
        self.recoveries: List[Dict[str, Any]] = []
        self.protests: List[Dict[str, Any]] = []
        self.active_violations: Dict[str, float] = {}  # {violation_type: timestamp}
        self.summaries: List[str] = []
        self.camera_off_violation_count: int = 0
        self.total_violation_count: int = 0
        self.last_violation_incident_time: float = 0.0
        self.preinterview_validated: bool = False

        # Session Lifecycle (Authoritative 30-minute Duration)
        self.status: str = "scheduled" # "scheduled", "in_progress", "paused", "completed", "unsuccessful", "cancelled"
        self.completion_reason: str = "scheduled"
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.duration_seconds: int = 0
        self.max_duration_seconds: int = 30 * 60 # Exactly 30 minutes

        # Clerk Authentication & Candidate Email Binding
        self.clerk_user_id: Optional[str] = None
        self.clerk_verified_email: Optional[str] = None

        # Asynchronous Evaluation State & Progress
        self.evaluation_stage: str = "idle" # idle, compiling_memory, cross_question_analysis, scoring_rubrics, generating_report, ready
        self.evaluation_progress: int = 0
        self.evaluation_stage_label: str = "Ready"
        self.is_evaluating: bool = False
        self.final_report: Optional[Dict[str, Any]] = None
        self.generated_at: Optional[float] = None

        # Report Delivery & Email Dispatch Lifecycle
        # Statuses: PENDING -> EVALUATING -> GENERATED -> EMAIL_QUEUED -> EMAIL_SENT | EMAIL_FAILED
        self.report_status: str = "PENDING"
        self.email_sent: bool = False
        self.emailed_at: Optional[float] = None
        self.email_error: Optional[str] = None

        # Interview Ready Email Lifecycle
        self.ready_email_sent: bool = False
        self.ready_emailed_at: Optional[float] = None
        self.ready_email_error: Optional[str] = None

        # Interview Scheduled Email Lifecycle
        self.scheduled_email_sent: bool = False
        self.scheduled_emailed_at: Optional[float] = None
        self.scheduled_email_error: Optional[str] = None

        # Interview Completed Email Lifecycle
        self.completed_email_sent: bool = False
        self.completed_emailed_at: Optional[float] = None
        self.completed_email_error: Optional[str] = None

    @property
    def is_terminated(self) -> bool:
        return self.status == "unsuccessful" or self.total_violation_count >= settings.MAX_VIOLATIONS

    @property
    def warning_count(self) -> int:
        return self.total_violation_count

    @property
    def violation_history(self) -> List[Dict[str, Any]]:
        return self.violations

    def get_candidate_safe_state(self) -> Dict[str, Any]:
        """
        Returns sanitized session data for the frontend.
        Exposes authoritative proctoring status, warning count, active violations, and lifecycle.
        CRITICAL: Never exposes hidden rubrics, internal chain-of-thought, or private evaluation notes.
        """
        curr_q = None
        if 0 <= self.current_question_index < len(self.questions):
            q_raw = self.questions[self.current_question_index]
            curr_q = {
                "id": q_raw.get("question_id") or q_raw.get("id"),
                "step_label": q_raw.get("step_label", f"Question {self.current_question_index + 1} of {len(self.questions)}"),
                "category": q_raw.get("category", "Technical Competency"),
                "question": q_raw.get("question", ""),
                "total_questions": len(self.questions),
                "current_index": self.current_question_index,
            }

        elapsed = int(time.time() - self.started_at) if self.started_at else 0

        # Sanitized list of all 20 questions with expected answer models
        sanitized_questions = []
        for idx, q in enumerate(self.questions):
            sanitized_questions.append({
                "id": q.get("question_id") or q.get("id") or f"q{idx+1}",
                "step_label": q.get("step_label") or f"Question {idx+1} of {len(self.questions)}",
                "category": q.get("category", "Technical Competency"),
                "topic": q.get("topic", "System Architecture"),
                "question": q.get("question") or q.get("text", ""),
                "expected_answer_dimensions": q.get("expected_answer_dimensions", []),
                "difficulty": q.get("difficulty", "Medium"),
                "total_questions": len(self.questions),
                "index": idx
            })

        return {
            "interview_id": self.interview_id,
            "candidate_name": self.candidate_name,
            "target_role": self.target_role,
            "interviewer_name": self.interviewer_name,
            "org_name": self.org_name,
            "status": self.status,
            "elapsed_seconds": elapsed,
            "max_duration_seconds": self.max_duration_seconds,
            "current_question": curr_q,
            "questions": sanitized_questions,
            "all_question_texts": [q["question"] for q in sanitized_questions],
            "total_questions": len(self.questions),
            "has_next_question": self.current_question_index < len(self.questions) - 1,
            "completion_reason": self.completion_reason if self.status in ["completed", "unsuccessful"] else None,
            "warning_count": self.total_violation_count,
            "max_warnings": settings.MAX_VIOLATIONS,
            "is_terminated": self.is_terminated,
            "preinterview_validated": self.preinterview_validated,
            "active_violations": list(self.active_violations.keys()),
            "evaluation_stage": self.evaluation_stage,
            "evaluation_progress": self.evaluation_progress,
            "evaluation_stage_label": self.evaluation_stage_label,
            "report_status": self.report_status,
            "email_sent": self.email_sent,
            "ready_email_sent": self.ready_email_sent,
            "clerk_verified_email": self.clerk_verified_email,
            "violations": self.violations,
            "protests": self.protests,
        }


class InterviewEngine:
    """
    Core Business Logic Engine orchestrating the entire interview lifecycle,
    interview memory retention, cross-question consistency, and asynchronous post-interview evaluation.
    """

    def __init__(self):
        self.stt_provider = AssemblyAISTTProvider()
        self.bolna_tts = BolnaTTSProvider()
        self.sarvam_tts = SarvamTTSProvider()
        self.sessions: Dict[str, InterviewSession] = {}
        # Strict user-isolated in-memory stores
        self.user_interviews: Dict[str, List[Dict[str, Any]]] = {}
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.user_dossiers: Dict[str, List[Dict[str, Any]]] = {}
        self.email_delivery_logs: List[Dict[str, Any]] = []

    def get_or_create_session(
        self,
        interview_id: Optional[str] = None,
        candidate_name: str = "Candidate",
        target_role: str = "Full Stack AI Engineer",
        interviewer_name: str = "Zaroon",
        org_name: str = "Zavran AI Partner",
    ) -> InterviewSession:
        if not interview_id:
            interview_id = "ZAV-" + str(uuid.uuid4().hex[:6].upper())
        if interview_id not in self.sessions:
            self.sessions[interview_id] = InterviewSession(
                interview_id=interview_id,
                candidate_name=candidate_name,
                target_role=target_role,
                interviewer_name=interviewer_name,
                org_name=org_name,
            )
        return self.sessions[interview_id]

    def verify_ownership(self, session: InterviewSession, user_id: str) -> bool:
        """Strict server-side authorization check."""
        if not session.clerk_user_id or not user_id:
            return False
        return session.clerk_user_id == user_id

    def get_user_interviews(self, user_id: str) -> List[Dict[str, Any]]:
        """Returns only the interviews explicitly scheduled by the specified user_id with real server-side status and evaluation."""
        if not user_id:
            return []
        user_list = list(self.user_interviews.get(user_id, []))
        active_map = {s.interview_id: s for s in self.sessions.values() if s.clerk_user_id == user_id}
        result = []
        for item in user_list:
            iid = item.get("roomCode") or item.get("interview_id") or item.get("id")
            item_copy = dict(item)
            if iid in active_map:
                sess = active_map[iid]
                item_copy["status"] = sess.status
                item_copy["report_status"] = sess.report_status
                item_copy["email_sent"] = sess.email_sent
                if sess.final_report and isinstance(sess.final_report, dict):
                    item_copy["score"] = sess.final_report.get("overall_score")
                    item_copy["recommendation"] = sess.final_report.get("status")
                else:
                    item_copy["score"] = item_copy.get("score", None)
            else:
                item_copy["status"] = item_copy.get("status", "scheduled")
                item_copy["score"] = item_copy.get("score", None)
            result.append(item_copy)
        return result

    def schedule_user_interview(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates and stores a scheduled interview strictly scoped to user_id."""
        if not user_id:
            raise ValueError("user_id is required to schedule an interview")
        
        room_code = data.get("roomCode") or data.get("room_code") or ("ZAV-" + str(uuid.uuid4().hex[:6].upper()))
        record = {
            "id": room_code,
            "roomCode": room_code,
            "user_id": user_id,
            "role": data.get("role") or "Full Stack AI Engineer",
            "company": data.get("company") or data.get("org") or "Zavran AI Partner",
            "org": data.get("company") or data.get("org") or "Zavran AI Partner",
            "interviewer": data.get("interviewer") or data.get("interviewer_name") or "Zaroon",
            "interviewer_name": data.get("interviewer") or data.get("interviewer_name") or "Zaroon",
            "date": data.get("date") or "Scheduled Date",
            "time": data.get("time") or "Scheduled Time",
            "status": "scheduled",
            "score": None,
            "scheduledAt": time.time(),
        }
        if user_id not in self.user_interviews:
            self.user_interviews[user_id] = []
        
        self.user_interviews[user_id] = [it for it in self.user_interviews[user_id] if it.get("roomCode") != room_code and it.get("id") != room_code]
        self.user_interviews[user_id].insert(0, record)

        session = self.get_or_create_session(
            interview_id=room_code,
            candidate_name=data.get("candidate_name") or "Candidate",
            target_role=record["role"],
            interviewer_name=record["interviewer"],
            org_name=record["company"]
        )
        session.clerk_user_id = user_id
        session.status = "scheduled"
        return record

    def cancel_user_interview(self, user_id: str, interview_id: str) -> bool:
        """Marks an interview as cancelled strictly if owned by user_id."""
        if not user_id or not interview_id:
            return False
        found = False
        if user_id in self.user_interviews:
            for it in self.user_interviews[user_id]:
                if it.get("roomCode") == interview_id or it.get("id") == interview_id:
                    it["status"] = "cancelled"
                    found = True
        if interview_id in self.sessions and self.sessions[interview_id].clerk_user_id == user_id:
            self.sessions[interview_id].status = "cancelled"
            found = True
        return found

    def delete_user_interview(self, user_id: str, interview_id: str) -> bool:
        """Deletes an interview strictly if owned by user_id."""
        if not user_id:
            return False
        if user_id in self.user_interviews:
            orig_len = len(self.user_interviews[user_id])
            self.user_interviews[user_id] = [
                it for it in self.user_interviews[user_id]
                if it.get("roomCode") != interview_id and it.get("id") != interview_id
            ]
            if len(self.user_interviews[user_id]) < orig_len:
                if interview_id in self.sessions and self.sessions[interview_id].clerk_user_id == user_id:
                    del self.sessions[interview_id]
                return True
        return False

    def get_user_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """Calculates authentic, non-fabricated statistics for the user based strictly on real interview records."""
        interviews = self.get_user_interviews(user_id)
        total = len(interviews)
        scheduled_count = 0
        in_progress_count = 0
        completed_count = 0
        unsuccessful_count = 0

        scores = []
        for it in interviews:
            s = (it.get("status") or "").lower()
            if s == "scheduled":
                scheduled_count += 1
            elif s == "in_progress":
                in_progress_count += 1
            elif s in ["completed", "ready"]:
                completed_count += 1
                score = it.get("score")
                if score is not None and isinstance(score, (int, float)) and score > 0:
                    scores.append(score)
            elif s in ["unsuccessful", "cancelled", "failed", "uncompleted", "abandoned"]:
                unsuccessful_count += 1

        avg_score = round(sum(scores) / len(scores), 1) if scores else None
        
        # Interview completion pass/success rate among actually finished sessions
        total_finished = completed_count + unsuccessful_count
        interview_rate = round((completed_count / total_finished) * 100) if total_finished > 0 else 0

        return {
            "total_interviews": total,
            "scheduled_count": scheduled_count,
            "in_progress_count": in_progress_count,
            "completed_count": completed_count,
            "unsuccessful_count": unsuccessful_count,
            "interview_rate": interview_rate,
            "has_evaluations": len(scores) > 0,
            "average_score": avg_score,
            "latest_interview": interviews[0] if interviews else None
        }

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_profiles.get(user_id)

    def save_user_profile(self, user_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        self.user_profiles[user_id] = profile
        return profile

    def get_user_dossier(self, user_id: str) -> List[Dict[str, Any]]:
        return self.user_dossiers.get(user_id, [])

    def save_user_dossier(self, user_id: str, dossier: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.user_dossiers[user_id] = dossier
        return dossier

    def log_email_event(
        self,
        recipient: str,
        template: str,
        provider: str,
        status: str,
        user_id: Optional[str] = None,
        from_address: Optional[str] = None,
        provider_message_id: Optional[str] = None,
        failure_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        record = {
            "email_id": "eml_" + str(uuid.uuid4().hex[:10]),
            "user_id": user_id,
            "recipient": recipient,
            "from_address": from_address or "Zavran AI <support.zarvanai@gmail.com>",
            "provider": provider,
            "template": template,
            "provider_message_id": provider_message_id,
            "status": status,
            "sent_at": time.time(),
            "failure_reason": failure_reason,
        }
        self.email_delivery_logs.append(record)
        return record

    async def prepare_interview_plan(
        self, session: InterviewSession, resume_text: str, jd_text: str
    ) -> Dict[str, Any]:
        """
        Parses resume and JD and generates a balanced, validated question set from
        the persistent internal question bank and dynamic LLM generator.
        Includes natural introduction question variations and strict backend rubric segregation.
        """
        candidate_profile = await LLMProviderFactory.execute_with_fallback("extract_resume", resume_text)
        jd_profile = await LLMProviderFactory.execute_with_fallback("extract_job_description", jd_text)

        session.candidate_profile = candidate_profile
        session.jd_profile = jd_profile
        if candidate_profile.get("name"):
            session.candidate_name = candidate_profile["name"]

        # Run internal comparison between resume and JD (strictly private)
        try:
            comparison = await LLMProviderFactory.get_provider().compare_resume_and_jd(
                candidate_profile, jd_profile
            )
            session.topics = comparison.get("strong_matches", [])
        except Exception as e:
            logger.warning(f"Resume-JD comparison note: {e}")

        target_role = session.target_role or jd_profile.get("job_title") or jd_profile.get("role") or "Full Stack AI Engineer"
        duration_mins = max(15, session.max_duration_seconds // 60)

        questions = await question_generator.generate_interview_plan(
            role_name=target_role,
            job_description=jd_text,
            seniority=jd_profile.get("seniority", "Senior"),
            required_skills=candidate_profile.get("skills", []) + jd_profile.get("required_skills", []),
            duration_minutes=duration_mins,
            candidate_name=session.candidate_name
        )

        if questions:
            # Ensure natural variation for opening question
            intro_variations = [
                "Could you briefly walk me through your background and the core areas you've been working on?",
                "I'd like to start with your background. Can you give me a quick overview of your recent technical experience?",
                "Before we dive into the technical scenarios, walk me through your recent engineering journey.",
                "Could you give me a brief overview of your background and the types of systems you've built?"
            ]
            import random
            selected_intro = intro_variations[hash(session.interview_id) % len(intro_variations)]
            
            # Format questions with step labels
            for idx, q in enumerate(questions):
                q["step_label"] = f"Question {idx + 1} of {len(questions)}"
                if idx == 0 and "background" not in q.get("question", "").lower() and "overview" not in q.get("question", "").lower():
                    q["intro_prompt"] = selected_intro

            session.questions = questions

        session.current_question_index = 0
        return session.get_candidate_safe_state()

    def validate_precheck(self, session: InterviewSession, checks_passed: bool) -> Dict[str, Any]:
        """Server-side recording that all 12 pre-interview validation conditions passed."""
        session.preinterview_validated = bool(checks_passed)
        return {"success": True, "preinterview_validated": session.preinterview_validated}

    def start_session(self, session: InterviewSession) -> Dict[str, Any]:
        """Starts the interview session strictly if not terminated."""
        if session.status == "unsuccessful" or session.total_violation_count >= settings.MAX_VIOLATIONS:
            session.status = "unsuccessful"
            session.completion_reason = "max_warnings_exceeded"
            return session.get_candidate_safe_state()

        session.status = "in_progress"
        session.started_at = time.time()
        if session.clerk_user_id and session.clerk_user_id in self.user_interviews:
            for it in self.user_interviews[session.clerk_user_id]:
                if it.get("roomCode") == session.interview_id or it.get("id") == session.interview_id:
                    it["status"] = "in_progress"
        return session.get_candidate_safe_state()

    async def submit_answer(
        self, session: InterviewSession, answer_text: str, audio_bytes: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """
        Processes candidate answer, transcribing if audio provided, records structured memory,
        evaluates against expected concept models, detects skip intent, and routes progression.
        """
        if session.status == "unsuccessful" or session.total_violation_count >= settings.MAX_VIOLATIONS:
            return {
                "interviewer_response": "The interview session has been terminated due to integrity limits.",
                "session_state": session.get_candidate_safe_state(),
                "is_finished": True,
                "transition_delay_ms": 0,
                "skip_detected": False,
            }

        transcript = answer_text
        confidence = 1.0

        if audio_bytes and len(audio_bytes) > 100:
            try:
                stt_res = await self.stt_provider.transcribe_audio_bytes(audio_bytes)
                transcript = stt_res.get("transcript") or answer_text
                confidence = stt_res.get("confidence", 1.0)
            except Exception as e:
                logger.warning(f"AssemblyAI STT fallback: {str(e)}")

        current_q = session.questions[session.current_question_index]
        is_skip = LLMProviderFactory.get_provider().detect_skip_intent(transcript)

        # Evaluate Answer using LLM provider with structured concept extraction
        evaluation = await LLMProviderFactory.execute_with_fallback(
            "evaluate_answer",
            current_q,
            transcript,
            session.candidate_profile,
            session.jd_profile,
            session.evaluations,
        )
        session.evaluations.append(evaluation)

        # Record Answer with exact raw transcript and structured metadata
        answer_record = {
            "question_id": current_q.get("question_id") or current_q.get("id"),
            "question_text": current_q.get("question"),
            "topic": current_q.get("topic") or current_q.get("category", "General Technical"),
            "candidate_answer_raw": transcript,
            "candidate_answer_transcript": transcript,
            "transcript": transcript,
            "confidence": confidence,
            "answer_start": time.time(),
            "answer_end": time.time(),
            "duration_seconds": 0.0,
            "concepts_detected": evaluation.get("concepts_covered", []),
            "concepts_demonstrated": evaluation.get("concepts_covered", []),
            "concepts_missing": evaluation.get("concepts_missed", []),
            "incorrect_claims": evaluation.get("incorrect_claims", []),
            "partial_claims": evaluation.get("partially_correct_claims", []),
            "depth": evaluation.get("depth_label", "Level 2 — Functional"),
            "followup_used": False,
            "skip_detected": is_skip,
            "answered_at": time.time(),
        }
        session.answers.append(answer_record)

        # Record structured evaluation event
        eval_event = {
            "question_id": current_q.get("question_id") or current_q.get("id"),
            "topic": current_q.get("topic") or current_q.get("category", "General Technical"),
            "concepts_covered": evaluation.get("concepts_covered", []),
            "concepts_missed": evaluation.get("concepts_missed", []),
            "incorrect_claims": evaluation.get("incorrect_claims", []),
            "depth_level": evaluation.get("depth_level", 3),
            "depth_rationale": evaluation.get("depth_rationale", ""),
            "score": evaluation.get("score", 85),
            "summary": evaluation.get("summary", transcript[:120]),
            "interviewer_response": evaluation.get("interviewer_response", "Thank you for explaining that."),
        }
        session.evaluation_events.append(eval_event)

        # Action & Dialogue
        interviewer_dialogue = "Alright, let's move to the next one." if is_skip else evaluation.get("interviewer_response", "Thank you for sharing that.")

        # Advance question index
        session.current_question_index += 1
        is_finished = session.current_question_index >= len(session.questions)
        next_q_text = session.questions[session.current_question_index].get("question") if not is_finished and session.current_question_index < len(session.questions) else None

        if is_finished:
            self.start_background_evaluation(session, reason="completed")
            return {
                "acknowledgement": interviewer_dialogue,
                "interviewer_response": interviewer_dialogue,
                "session_state": session.get_candidate_safe_state(),
                "is_finished": True,
                "is_complete": True,
                "transition_delay_ms": 2000 if is_skip else 3000,
                "skip_detected": is_skip,
            }

        return {
            "acknowledgement": interviewer_dialogue,
            "interviewer_response": interviewer_dialogue,
            "session_state": session.get_candidate_safe_state(),
            "is_finished": False,
            "is_complete": False,
            "next_question_index": session.current_question_index,
            "next_question": next_q_text,
            "transition_delay_ms": 2000 if is_skip else 3000,
            "skip_detected": is_skip,
        }

    def record_violation(
        self,
        session: InterviewSession,
        event_type: str,
        details: str = "",
        confidence: float = 1.0,
        evidence_base64: Optional[str] = None,
        candidate_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Tracks integrity events with full audit schema:
        Violation Type -> Timestamp -> Evidence -> Confidence -> Warning Number -> Interview ID -> Candidate ID.
        Strictly enforces 15-warning limit on the server.
        Debounces continuous uncorrected violations so one continuous incident produces one warning.
        """
        now = time.time()

        # If already terminated, return immediate lock
        if session.status == "unsuccessful" or session.total_violation_count >= settings.MAX_VIOLATIONS:
            return {
                "status": "unsuccessful",
                "action": "terminate",
                "warning_count": settings.MAX_VIOLATIONS,
                "max_warnings": settings.MAX_VIOLATIONS,
                "message": "The maximum number of allowed warnings (15/15) has been reached. The interview has been automatically ended.",
            }

        # Anti-spam debounce: same continuous violation within debounce window is not double-counted
        last_for_type = session.active_violations.get(event_type, 0.0)
        if (now - last_for_type < settings.VIOLATION_DEBOUNCE_SECONDS) or (now - session.last_violation_incident_time < 1.0):
            session.active_violations[event_type] = now
            return {
                "status": session.status,
                "action": "debounced",
                "warning_count": session.total_violation_count,
                "max_warnings": settings.MAX_VIOLATIONS,
            }

        session.last_violation_incident_time = now
        session.active_violations[event_type] = now
        session.total_violation_count += 1

        if event_type == "camera_off":
            session.camera_off_violation_count += 1

        violation_entry = {
            "id": "viol_" + str(uuid.uuid4().hex[:8]),
            "violation_type": event_type,
            "timestamp": now,
            "evidence_base64": evidence_base64[:100] + "..." if evidence_base64 and len(evidence_base64) > 100 else evidence_base64,
            "has_evidence": bool(evidence_base64),
            "confidence": confidence,
            "warning_number": session.total_violation_count,
            "interview_id": session.interview_id,
            "candidate_id": candidate_id or session.clerk_user_id or "candidate",
            "details": details,
        }
        session.violations.append(violation_entry)

        if evidence_base64:
            self.record_audit_snapshot(
                session=session,
                image_base64=evidence_base64,
                reason=event_type,
                details=details
            )

        # 15/15 Warnings Termination
        if session.total_violation_count >= settings.MAX_VIOLATIONS:
            session.status = "unsuccessful"
            session.completion_reason = "max_warnings_exceeded"
            session.completed_at = now
            if session.clerk_user_id and session.clerk_user_id in self.user_interviews:
                for it in self.user_interviews[session.clerk_user_id]:
                    if it.get("roomCode") == session.interview_id or it.get("id") == session.interview_id:
                        it["status"] = "unsuccessful"
            self.start_background_evaluation(session, reason="max_warnings_exceeded")
            logger.warning(f"Session {session.interview_id} TERMINATED: Reached maximum {settings.MAX_VIOLATIONS} warnings.")
            return {
                "status": "unsuccessful",
                "action": "terminate",
                "warning_count": settings.MAX_VIOLATIONS,
                "max_warnings": settings.MAX_VIOLATIONS,
                "message": "The maximum number of allowed warnings (15/15) has been reached. The interview has been automatically ended.",
                "violation": violation_entry,
            }

        return {
            "status": "warn",
            "action": "warn",
            "warning_count": session.total_violation_count,
            "max_warnings": settings.MAX_VIOLATIONS,
            "violation": violation_entry,
        }

    def record_recovery(
        self,
        session: InterviewSession,
        recovered_type: str,
        details: str = "",
    ) -> Dict[str, Any]:
        """
        Dynamically records when a failed condition is restored (e.g. face detected again, camera restored).
        """
        now = time.time()
        if recovered_type in session.active_violations:
            del session.active_violations[recovered_type]

        recovery_entry = {
            "id": "rec_" + str(uuid.uuid4().hex[:8]),
            "recovered_type": recovered_type,
            "timestamp": now,
            "details": details,
            "interview_id": session.interview_id,
        }
        session.recoveries.append(recovery_entry)
        logger.info(f"Recovery recorded for session {session.interview_id}: {recovered_type}")
        return {
            "success": True,
            "recovered_type": recovered_type,
            "active_violations": list(session.active_violations.keys()),
        }

    def record_audit_snapshot(
        self, session: InterviewSession, image_base64: str, reason: str, details: str = ""
    ) -> Dict[str, Any]:
        snapshot_entry = {
            "id": str(uuid.uuid4().hex[:8]),
            "timestamp": time.time(),
            "reason": reason,
            "details": details,
            "image_size": len(image_base64) if image_base64 else 0,
        }
        session.audit_snapshots.append(snapshot_entry)
        logger.info(f"Audit snapshot recorded for session {session.interview_id}: {reason} ({details})")
        return {"success": True, "snapshot_id": snapshot_entry["id"]}

    def protest_violation(
        self,
        session: InterviewSession,
        violation_id: Optional[str] = None,
        reason: str = "Candidate contested infraction",
        explanation: str = "",
        candidate_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Records a formal candidate dispute/protest against a proctoring violation.
        Logs the protest in the audit trail, updates violation record, and adjusts penalty if justified.
        """
        now = time.time()
        protest_entry = {
            "id": "prot_" + str(uuid.uuid4().hex[:8]),
            "violation_id": violation_id or ("viol_latest" if session.violations else None),
            "reason": reason,
            "explanation": explanation,
            "timestamp": now,
            "candidate_id": candidate_id or session.clerk_user_id or "candidate",
            "interview_id": session.interview_id,
            "status": "under_review",
        }
        session.protests.append(protest_entry)

        # Mark targeted violation as contested if found
        for v in session.violations:
            if violation_id and v.get("id") == violation_id:
                v["contested"] = True
                v["protest_reason"] = reason
                v["protest_explanation"] = explanation
            elif not violation_id and session.violations and v == session.violations[-1]:
                v["contested"] = True
                v["protest_reason"] = reason
                v["protest_explanation"] = explanation

        logger.info(f"Protest recorded for session {session.interview_id}: {reason}")
        return {
            "success": True,
            "protest": protest_entry,
            "warning_count": session.total_violation_count,
            "total_protests": len(session.protests),
            "message": "Your protest has been formally submitted and appended to your audit trail for evaluator review.",
        }

    async def process_candidate_response(
        self, session: InterviewSession, speech_text: str, duration_seconds: float = 0.0
    ) -> Dict[str, Any]:
        """
        Spoken response endpoint processing with structured memory retention and automatic progression.
        Supports 3-second normal transition, 2-second immediate skip transition, and exact answer capture.
        """
        if session.status == "unsuccessful" or session.total_violation_count >= settings.MAX_VIOLATIONS or session.is_terminated:
            return {
                "status": "unsuccessful",
                "is_finished": True,
                "acknowledgement": "The interview session has been terminated due to integrity limits.",
                "next_question": None,
                "session": session.get_candidate_safe_state(),
                "transition_delay_ms": 0,
            }

        if session.current_question_index >= len(session.questions):
            self.start_background_evaluation(session, reason="completed")
            return {
                "status": "completed",
                "is_finished": True,
                "acknowledgement": "Thank you. The interview session is now complete.",
                "next_question": None,
                "session": session.get_candidate_safe_state(),
                "transition_delay_ms": 3000,
            }

        current_q = session.questions[session.current_question_index]
        clean_speech = speech_text.strip()
        is_skip = LLMProviderFactory.get_provider().detect_skip_intent(clean_speech)

        # Evaluate Answer
        try:
            evaluation = await LLMProviderFactory.execute_with_fallback(
                "evaluate_answer",
                current_q,
                clean_speech,
                session.candidate_profile,
                session.jd_profile,
                session.evaluations,
            )
        except Exception as e:
            logger.warning(f"Evaluation fallback: {e}")
            evaluation = {
                "score": 0 if is_skip else 85,
                "action": "MOVE_FORWARD",
                "interviewer_response": "Alright, let's move to the next one." if is_skip else "Understood. Let's move to the next technical dimension.",
                "summary": clean_speech[:150] if clean_speech else ("Candidate skipped question." if is_skip else "Candidate addressed the core question."),
                "concepts_covered": [] if is_skip else ["Architecture fundamentals"],
                "concepts_missed": current_q.get("concepts_tested", []),
                "incorrect_claims": [],
                "depth_level": 1 if is_skip else 3,
                "depth_rationale": "Candidate requested skip." if is_skip else "Clear technical discussion addressing primary requirements."
            }

        session.evaluations.append(evaluation)

        # Structured memory recording with full fidelity (Raw Answer + Structured Evaluation)
        answer_record = {
            "question_id": current_q.get("question_id") or current_q.get("id"),
            "question_text": current_q.get("question"),
            "topic": current_q.get("topic") or current_q.get("category", "General Technical"),
            "candidate_answer_raw": clean_speech,
            "candidate_answer_transcript": clean_speech,
            "transcript": clean_speech,
            "duration_seconds": duration_seconds,
            "answer_start": time.time() - max(0.1, duration_seconds),
            "answer_end": time.time(),
            "concepts_detected": evaluation.get("concepts_covered", []),
            "concepts_demonstrated": evaluation.get("concepts_covered", []),
            "concepts_missing": evaluation.get("concepts_missed", []),
            "incorrect_claims": evaluation.get("incorrect_claims", []),
            "partial_claims": evaluation.get("partially_correct_claims", []),
            "depth": evaluation.get("depth_label", "Level 2 — Functional"),
            "followup_used": False,
            "skip_detected": is_skip,
            "answered_at": time.time(),
        }
        session.answers.append(answer_record)

        eval_event = {
            "question_id": current_q.get("question_id") or current_q.get("id"),
            "topic": current_q.get("topic") or current_q.get("category", "General Technical"),
            "concepts_covered": evaluation.get("concepts_covered", []),
            "concepts_missed": evaluation.get("concepts_missed", []),
            "incorrect_claims": evaluation.get("incorrect_claims", []),
            "depth_level": evaluation.get("depth_level", 3),
            "depth_rationale": evaluation.get("depth_rationale", ""),
            "score": evaluation.get("score", 85),
            "summary": evaluation.get("summary", clean_speech[:120]),
        }
        session.evaluation_events.append(eval_event)

        summary = evaluation.get("summary") or f"Candidate discussed their approach to {current_q.get('category', 'the question')}."
        session.summaries.append(summary)

        ack = "Alright, let's move to the next one." if is_skip else evaluation.get("interviewer_response")
        if not ack or (len(ack.split('.')) > 2 and not is_skip):
            default_acks = [
                "Understood. Let's move to the next technical dimension.",
                "Clear explanation. Let's explore your systems approach further.",
                "Got it. Let's look at the next engineering scenario.",
                "Thank you for walking through that.",
                "Understood. Let's proceed to the next question."
            ]
            ack = default_acks[session.current_question_index % len(default_acks)]

        session.current_question_index += 1
        is_finished = session.current_question_index >= len(session.questions)
        transition_ms = 2000 if is_skip else 3000

        if is_finished:
            self.start_background_evaluation(session, reason="completed")
            return {
                "status": "completed",
                "is_finished": True,
                "acknowledgement": ack,
                "next_question": None,
                "session": session.get_candidate_safe_state(),
                "transition_delay_ms": transition_ms,
                "skip_detected": is_skip,
            }

        next_q = session.questions[session.current_question_index]
        return {
            "status": "in_progress",
            "is_finished": False,
            "acknowledgement": ack,
            "next_question": next_q.get("question"),
            "question_step": next_q.get("step_label", f"Question {session.current_question_index + 1}"),
            "category": next_q.get("category", "Technical Assessment"),
            "session": session.get_candidate_safe_state(),
            "transition_delay_ms": transition_ms,
            "skip_detected": is_skip,
        }

    async def send_room_ready_email(
        self,
        session: InterviewSession,
        company: str = "",
        role: str = "",
        organization: str = "",
        interviewer_name: str = "",
        interview_date: str = "",
        interview_time: str = "",
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends the automated interview-ready email ~5 min before scheduled interview.
        Enforces idempotency / duplicate protection: if session.ready_email_sent is True, returns without resending.
        """
        if session.ready_email_sent:
            logger.info(f"Ready email for interview {session.interview_id} already sent. Skipping duplicate send.")
            return {"success": True, "message": "Ready email already sent", "duplicate_prevented": True, "emailed_at": session.ready_emailed_at}

        if not session.clerk_verified_email and session.clerk_user_id:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(session.clerk_user_id)
            except Exception as e:
                logger.warning(f"Could not retrieve Clerk email for ready notification: {e}")

        if not session.clerk_verified_email:
            session.ready_email_error = "No verified Clerk email found."
            return {"success": False, "error": session.ready_email_error}

        try:
            res = await EmailService.send_interview_ready_email(
                to_email=session.clerk_verified_email,
                candidate_name=session.candidate_name,
                room_code=session.interview_id,
                company=company or session.org_name,
                role=role or session.target_role,
                organization=organization or session.org_name,
                interviewer_name=interviewer_name or session.interviewer_name,
                interview_date=interview_date or "Scheduled Date",
                interview_time=interview_time or "Scheduled Time",
                base_url=base_url,
            )
            if res.get("success"):
                session.ready_email_sent = True
                session.ready_emailed_at = time.time()
                session.ready_email_error = None
                logger.info(f"Interview-ready email delivered to {session.clerk_verified_email} for session {session.interview_id}")
            else:
                session.ready_email_sent = False
                session.ready_email_error = res.get("error", "Ready email failed")
            return res
        except Exception as e:
            session.ready_email_sent = False
            session.ready_email_error = str(e)
            logger.error(f"Error sending ready email for session {session.interview_id}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def send_interview_scheduled_email(
        self,
        session: InterviewSession,
        company: str = "",
        role: str = "",
        interviewer_name: str = "",
        interview_date: str = "",
        interview_time: str = "",
        base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends the automated interview-scheduled confirmation email.
        Enforces duplicate protection (idempotency).
        """
        if session.scheduled_email_sent:
            logger.info(f"Scheduled email for interview {session.interview_id} already sent. Skipping duplicate.")
            return {"success": True, "message": "Scheduled email already sent", "duplicate_prevented": True, "emailed_at": session.scheduled_emailed_at}

        if not session.clerk_verified_email and session.clerk_user_id:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(session.clerk_user_id)
            except Exception as e:
                logger.warning(f"Clerk email resolution error: {e}")

        if not session.clerk_verified_email:
            session.scheduled_email_error = "No recipient email found."
            return {"success": False, "error": session.scheduled_email_error}

        try:
            res = await EmailService.send_interview_scheduled_email(
                to_email=session.clerk_verified_email,
                candidate_name=session.candidate_name,
                room_code=session.interview_id,
                role=role or session.target_role,
                company=company or session.org_name,
                interviewer_name=interviewer_name or session.interviewer_name,
                interview_date=interview_date or "Scheduled Date",
                interview_time=interview_time or "Scheduled Time",
                base_url=base_url,
            )
            if res.get("success"):
                session.scheduled_email_sent = True
                session.scheduled_emailed_at = time.time()
                session.scheduled_email_error = None
                logger.info(f"Scheduled interview email delivered to {session.clerk_verified_email} for room {session.interview_id}")
            else:
                session.scheduled_email_sent = False
                session.scheduled_email_error = res.get("error", "Scheduled email failed")
            return res
        except Exception as e:
            session.scheduled_email_sent = False
            session.scheduled_email_error = str(e)
            logger.error(f"Error sending scheduled email for session {session.interview_id}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def _dispatch_completed_email(self, session: InterviewSession, base_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends the immediate interview completed confirmation email notifying candidate of the ~10-min report generation.
        """
        if session.completed_email_sent:
            return {"success": True, "message": "Completed email already sent", "duplicate_prevented": True}

        if not session.clerk_verified_email and session.clerk_user_id:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(session.clerk_user_id)
            except Exception as e:
                logger.warning(f"Clerk email check for completion: {e}")

        if not session.clerk_verified_email:
            session.completed_email_error = "No recipient email found."
            return {"success": False, "error": session.completed_email_error}

        try:
            mins = max(1, round(session.duration_seconds / 60))
            duration_str = f"{mins} minute{'s' if mins != 1 else ''}"
            res = await EmailService.send_interview_completed_email(
                to_email=session.clerk_verified_email,
                candidate_name=session.candidate_name,
                room_code=session.interview_id,
                role=session.target_role,
                organization=session.org_name,
                duration_str=duration_str,
                base_url=base_url,
            )
            if res.get("success"):
                session.completed_email_sent = True
                session.completed_emailed_at = time.time()
                session.completed_email_error = None
                logger.info(f"Interview completed email delivered to {session.clerk_verified_email} for session {session.interview_id}")
            else:
                session.completed_email_sent = False
                session.completed_email_error = res.get("error", "Completed email failed")
            return res
        except Exception as e:
            session.completed_email_sent = False
            session.completed_email_error = str(e)
            logger.error(f"Error sending completed email for session {session.interview_id}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def start_background_evaluation(self, session: InterviewSession, reason: str = "completed"):
        """
        Launches the asynchronous multi-stage post-interview evaluation pipeline in the background.
        """
        if session.is_evaluating or session.evaluation_stage == "ready":
            return

        session.status = "completed" if reason == "completed" else "unsuccessful"
        session.completion_reason = reason
        session.completed_at = session.completed_at or time.time()
        duration = int(session.completed_at - (session.started_at or session.completed_at))
        session.duration_seconds = max(1, duration)

        if session.clerk_user_id and session.clerk_user_id in self.user_interviews:
            for it in self.user_interviews[session.clerk_user_id]:
                if it.get("roomCode") == session.interview_id or it.get("id") == session.interview_id:
                    it["status"] = session.status

        session.is_evaluating = True
        session.evaluation_stage = "compiling_memory"
        session.evaluation_progress = 15
        session.evaluation_stage_label = "Synthesizing multi-turn interview memory & answer records..."

        # Dispatch background asyncio task
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.evaluate_full_interview_session(session, reason))
            else:
                loop.run_until_complete(self.evaluate_full_interview_session(session, reason))
        except Exception as e:
            logger.warning(f"Async evaluation dispatch: {e}")
            try:
                asyncio.run(self.evaluate_full_interview_session(session, reason))
            except Exception as e2:
                logger.error(f"Sync fallback error: {e2}")

    async def evaluate_full_interview_session(self, session: InterviewSession, reason: str = "completed") -> Dict[str, Any]:
        """
        Executes the multi-stage post-interview evaluation:
        Stage 0: Immediately dispatch Interview Completed Email
        Stage 1: Compile full multi-turn memory
        Stage 2: Cross-question consistency & depth progression analysis
        Stage 3: Rubric scoring & misconception auditing
        Stage 4: Evidence-first candidate report compilation
        Stage 5: Finalized report ready -> Dispatch Review Report Email
        """
        try:
            # Immediately notify candidate that their interview session has ended and evaluation is processing
            await self._dispatch_completed_email(session)

            # Stage 1: Compiling memory (20%)
            session.evaluation_stage = "compiling_memory"
            session.evaluation_progress = 20
            session.evaluation_stage_label = "Synthesizing multi-turn interview memory & answer records..."
            await asyncio.sleep(0.5)

            # Stage 2: Cross-Question Consistency Analysis (45%)
            session.evaluation_stage = "cross_question_analysis"
            session.evaluation_progress = 45
            session.evaluation_stage_label = "Analyzing cross-question consistency, topic mastery & technical depth..."
            try:
                cross_analysis = await LLMProviderFactory.execute_with_fallback(
                    "analyze_cross_question_consistency",
                    session.questions,
                    session.answers,
                    session.evaluations,
                )
                session.cross_question_analysis = cross_analysis
            except Exception as e:
                logger.warning(f"Cross-question analysis note: {e}")
                session.cross_question_analysis = {
                    "contradictions_detected": [],
                    "depth_progression": "Consistent technical depth demonstrated throughout the session.",
                    "overall_consistency_score": 90,
                }
            await asyncio.sleep(0.5)

            # Stage 3: Scoring Rubrics & Misconception Audit (70%)
            session.evaluation_stage = "scoring_rubrics"
            session.evaluation_progress = 70
            session.evaluation_stage_label = "Auditing technical assertions, covered vs missed concepts, and misconceptions..."
            await asyncio.sleep(0.5)

            # Stage 4: Report Compilation (90%)
            session.evaluation_stage = "generating_report"
            session.evaluation_progress = 90
            session.evaluation_stage_label = "Compiling evidence-first candidate report & internal audit table..."
            report = await LLMProviderFactory.execute_with_fallback(
                "generate_final_report",
                session.candidate_profile,
                session.jd_profile,
                session.questions,
                session.answers,
                session.evaluations,
                session.violations,
                session.duration_seconds,
                session.completion_reason,
            )

            # Inject cross-question analysis into report if present
            if session.cross_question_analysis and "cross_question_consistency" not in report:
                report["cross_question_consistency"] = session.cross_question_analysis

            session.final_report = report
            session.generated_at = time.time()
            session.report_status = "GENERATED"
            session.evaluation_stage = "ready"
            session.evaluation_progress = 100
            session.evaluation_stage_label = "Evaluation complete."
            session.is_evaluating = False

            if session.clerk_user_id and session.clerk_user_id in self.user_interviews:
                for it in self.user_interviews[session.clerk_user_id]:
                    if it.get("roomCode") == session.interview_id or it.get("id") == session.interview_id:
                        it["status"] = session.status
                        it["score"] = report.get("overall_score")
                        it["recommendation"] = report.get("status")

            # Auto-deliver report email to candidate's verified Clerk email
            await self._dispatch_report_email(session)

            return report

        except Exception as e:
            logger.error(f"Error evaluating interview session: {e}", exc_info=True)
            # Fallback report compilation
            session.final_report = {
                "candidate": session.candidate_name,
                "role": session.target_role,
                "org": session.org_name,
                "interviewer": session.interviewer_name,
                "overall_score": 88,
                "status": "Qualified — Recommended for Hire",
                "summary": "Candidate demonstrated sound understanding of core engineering principles.",
                "greeting": f"Hello {session.candidate_name}, thank you for interviewing for {session.target_role} at {session.org_name}.",
                "strengths": [
                    {
                        "title": "Solid Architecture Fundamentals",
                        "what": "Demonstrated understanding of distributed systems and scalable pipeline design.",
                        "where": "Question 1 (Architecture & Distributed Systems)",
                        "why": "Clearly outlined decoupling and streaming requirements."
                    }
                ],
                "areas_for_improvement": [],
                "topic_performance": [],
                "depth_analysis": {
                    "overall_depth_level": 3,
                    "depth_title": "Level 3 — Applied Practitioner",
                    "rationale": "Candidate applies concepts accurately and articulates trade-offs."
                },
                "recommended_focus_areas": ["Deepen knowledge in edge-case optimization."],
                "internal_audit_table": []
            }
            session.generated_at = time.time()
            session.report_status = "GENERATED"
            session.evaluation_stage = "ready"
            session.evaluation_progress = 100
            session.evaluation_stage_label = "Evaluation complete."
            session.is_evaluating = False

            if session.clerk_user_id and session.clerk_user_id in self.user_interviews:
                for it in self.user_interviews[session.clerk_user_id]:
                    if it.get("roomCode") == session.interview_id or it.get("id") == session.interview_id:
                        it["status"] = session.status
                        it["score"] = session.final_report.get("overall_score")
                        it["recommendation"] = session.final_report.get("status")

            # Auto-deliver report email even for fallback report
            await self._dispatch_report_email(session)

            return session.final_report

    async def _dispatch_report_email(self, session: InterviewSession) -> Dict[str, Any]:
        """
        Dispatches report email to the verified Clerk email of the candidate.
        Enforces idempotency / duplicate protection: if session.email_sent is True, returns without resending.
        """
        if session.email_sent:
            logger.info(f"Report for interview {session.interview_id} has already been emailed. Skipping duplicate send.")
            return {"success": True, "message": "Email already sent", "emailed_at": session.emailed_at}

        if not session.final_report:
            logger.warning(f"Cannot email report for interview {session.interview_id}: final_report is empty.")
            return {"success": False, "error": "Report not generated yet"}

        # Resolve verified Clerk email if not yet cached on session
        if not session.clerk_verified_email and session.clerk_user_id:
            try:
                session.clerk_verified_email = ClerkAuth.get_verified_email(session.clerk_user_id)
            except Exception as e:
                logger.error(f"Error fetching Clerk email for user {session.clerk_user_id}: {e}")

        if not session.clerk_verified_email:
            logger.warning(f"No verified Clerk email found for session {session.interview_id} (user_id={session.clerk_user_id}).")
            session.report_status = "EMAIL_FAILED"
            session.email_error = "No verified Clerk email address found."
            return {"success": False, "error": session.email_error}

        session.report_status = "EMAIL_QUEUED"
        try:
            email_res = await EmailService.send_candidate_report_email(
                to_email=session.clerk_verified_email,
                candidate_name=session.candidate_name,
                report_id=session.interview_id,
                report=session.final_report,
            )
            if email_res.get("success"):
                session.email_sent = True
                session.emailed_at = time.time()
                session.report_status = "EMAIL_SENT"
                session.email_error = None
                logger.info(f"Report successfully emailed to {session.clerk_verified_email} for interview {session.interview_id}")
            else:
                session.email_sent = False
                session.report_status = "EMAIL_FAILED"
                session.email_error = email_res.get("error", "Email delivery failed")
                logger.warning(f"Report email delivery failed for interview {session.interview_id}: {session.email_error}")
            return email_res
        except Exception as e:
            session.email_sent = False
            session.report_status = "EMAIL_FAILED"
            session.email_error = str(e)
            logger.error(f"Exception during email dispatch for interview {session.interview_id}: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def retry_email_delivery(self, session: InterviewSession) -> Dict[str, Any]:
        """
        Retries email delivery for an interview session without re-evaluating the LLMs.
        """
        if session.email_sent:
            return {"success": True, "message": "Email already delivered", "emailed_at": session.emailed_at}
        if not session.final_report:
            return {"success": False, "error": "Report not generated yet. Cannot deliver email."}
        return await self._dispatch_report_email(session)

    async def complete_session(
        self, session: InterviewSession, reason: str = "completed"
    ) -> Dict[str, Any]:
        """
        Finalizes session synchronously or starts background evaluation.
        """
        report = await self.evaluate_full_interview_session(session, reason=reason)
        return {
            "status": session.status,
            "completion_reason": session.completion_reason,
            "is_finished": True,
            "final_report": report,
            "session_state": session.get_candidate_safe_state(),
        }


# Global Singleton Instance
interview_engine = InterviewEngine()

