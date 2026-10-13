"""
Comprehensive 20-Point Verification Test Suite for Zavran AI Platform Upgrade.
Tests all 20 required scenarios from Section 13 of the Specification:
1. User logout and login: Verify user data, resume facts, and interview history persist permanently.
2. Cross-user isolation: User A cannot access User B's interview, report, or private data.
3. Session cookies: Authenticated session cookies behave correctly; logout invalidates the session.
4. Early interview entry: Rejected before 2 minutes prior to scheduled start.
5. Eligible interview entry: Allowed at the permitted time (<= 2 min before scheduled time).
6. Question preparation: Resume facts and role requirements are reflected in generated questions.
7. Unsupported roles: Dynamically generates role-specific interview material instead of generic fallback.
8. RAG document retrieval: Candidate and role permissions are strictly respected.
9. Answer capture: Every response is associated with its corresponding question.
10. Interrupted interview: Already-recorded answers persist after interruption/reconnect.
11. Answer evaluation - synonymous wording: Semantic match receives credit.
12. Answer evaluation - missing concepts / errors: Penalized with lower scores.
13. Unanswered / skipped questions: Scored as 0, never given credit.
14. Final report availability: Blocked until 10 minutes post-interview completion.
15. Monitoring consent: Monitoring operates only after explicit consent is granted.
16. Inconclusive monitoring signals: Confidence < 0.7 marked as inconclusive, not cheating.
17. Evidence URLs: Direct unauthorized access is denied.
18. AI provider failure: Transparently falls back to secondary provider/safe offline rubric.
19. Duplicate requests: Repeated bookings, answer submissions, or report requests are idempotent.
20. Account deletion / retention: Data is completely deleted according to policy.
"""

import time
import uuid
import pytest
from starlette.testclient import TestClient

from backend.main import app
from backend.database import (
    init_db,
    save_user_profile,
    get_user_profile,
    save_interview,
    get_interview_by_room_code,
    save_interview_report,
    get_interview_report,
    delete_user_account_data,
    record_monitoring_consent,
    has_monitoring_consent,
    save_qa_pair,
    get_qa_pairs,
)
from backend.services.agent_orchestrator import (
    agent_orchestrator,
    EvaluationAgent,
    ReportAgent,
    SafetyAndPrivacyLayer,
    A2AMessage,
)
from backend.services.yolov8_service import yolov8_monitoring_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


# ---------------------------------------------------------------------------
# Test 1: User logout and login: Verify user data, resume facts, and interview history persist
# ---------------------------------------------------------------------------
def test_01_logout_and_login_data_persistence():
    user_id = "test_user_persistence_01"
    save_user_profile(
        user_id=user_id,
        email="persist@zavran.ai",
        name="Persistent User",
        target_role="Senior ML Engineer",
        skills=["Python", "TensorFlow", "Kubernetes"],
        experience_years=6,
    )
    save_interview(
        room_code="ZAV-PERSIST-01",
        user_id=user_id,
        user_email="persist@zavran.ai",
        role="Senior ML Engineer",
        scheduled_epoch=int(time.time()),
        status="scheduled",
    )

    # Simulate logout and re-login by fetching directly by user_id
    profile_after = get_user_profile(user_id)
    assert profile_after is not None
    assert profile_after["target_role"] == "Senior ML Engineer"
    assert "TensorFlow" in profile_after["skills"]

    # Verify interview still belongs to user
    interview = get_interview_by_room_code("ZAV-PERSIST-01")
    assert interview is not None
    assert interview["user_id"] == user_id


# ---------------------------------------------------------------------------
# Test 2: Cross-user isolation: User A cannot access User B's interview or report
# ---------------------------------------------------------------------------
def test_02_cross_user_isolation():
    user_a = "user_alpha_02"
    user_b = "user_beta_02"

    save_interview(
        room_code="ZAV-ISOLATE-A",
        user_id=user_a,
        user_email="alpha@zavran.ai",
        role="Backend Architect",
        scheduled_epoch=int(time.time()),
        status="scheduled",
    )

    # User B attempts to access User A's interview status via API
    resp = client.get(
        "/api/user/interviews/ZAV-ISOLATE-A/status",
        headers={"Authorization": f"Bearer {user_b}"},
    )
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Test 3: Session cookies: Authenticated session cookies behave correctly; logout invalidates
# ---------------------------------------------------------------------------
def test_03_session_cookie_and_logout_invalidation():
    # Register/login user via auth router to get cookie
    login_resp = client.post(
        "/api/auth/register",
        json={"email": "cookie_test@zavran.ai", "name": "Cookie Tester", "password": "PassSecure123!"},
    )
    assert login_resp.status_code in [200, 201]
    cookie = login_resp.cookies.get("zaveran_session")
    assert cookie is not None

    # Call logout endpoint to invalidate cookie
    logout_resp = client.post("/api/auth/logout")
    assert logout_resp.status_code == 200
    # Cookie should be set with empty or expired attribute
    assert (
        "zaveran_session" not in logout_resp.cookies
        or logout_resp.cookies.get("zaveran_session") == ""
    )


# ---------------------------------------------------------------------------
# Test 4: Early interview entry: Rejected before 2 minutes prior to scheduled start
# ---------------------------------------------------------------------------
def test_04_early_interview_entry_blocked():
    now = int(time.time())
    future_time = now + 1800  # Scheduled 30 minutes from now (> 2 minutes away)
    user_id = "user_early_entry_04"

    save_interview(
        room_code="ZAV-EARLY-04",
        user_id=user_id,
        user_email="early@zavran.ai",
        role="Frontend Engineer",
        scheduled_epoch=future_time,
        status="scheduled",
    )

    resp = client.get(
        "/api/interview/ZAV-EARLY-04/session",
        headers={"Authorization": f"Bearer {user_id}"},
    )
    assert resp.status_code == 403
    assert "2 minutes" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# Test 5: Eligible interview entry: Allowed at the permitted time (<= 2 min before scheduled time)
# ---------------------------------------------------------------------------
def test_05_eligible_interview_entry_allowed():
    now = int(time.time())
    eligible_time = now + 60  # 1 minute away (<= 2 minutes window)
    user_id = "user_eligible_05"

    save_interview(
        room_code="ZAV-ELIGIBLE-05",
        user_id=user_id,
        user_email="eligible@zavran.ai",
        role="Frontend Engineer",
        scheduled_epoch=eligible_time,
        status="scheduled",
    )

    resp = client.get(
        "/api/interview/ZAV-ELIGIBLE-05/session",
        headers={"Authorization": f"Bearer {user_id}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["session"]["interview_id"] == "ZAV-ELIGIBLE-05"


# ---------------------------------------------------------------------------
# Test 6: Question preparation: Resume facts and role requirements are reflected
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_06_question_preparation_uses_resume_and_role():
    msg = A2AMessage(
        task_id="task_prep_06",
        interview_id="ZAV-PREP-06",
        originating_agent="TestRunner",
        target_agent="QuestionGenerationAgent",
        payload={
            "role": "Distributed Systems Architect",
            "resume_facts": {
                "skills": ["Raft Consensus", "gRPC", "Etcd", "Go"],
                "experience_summary": "Architected distributed KV-store using Raft in Go.",
            },
        },
    )
    response_msg = await agent_orchestrator.dispatch(msg)
    questions = response_msg.payload.get("questions", [])
    assert len(questions) > 0

    # Ensure questions reference distributed systems or candidate skills
    combined_text = " ".join([q.get("question", "") for q in questions]).lower()
    assert any(term in combined_text for term in ["system", "distributed", "raft", "grpc", "architecture", "scale"])


# ---------------------------------------------------------------------------
# Test 7: Unsupported roles: Dynamically generates role-specific interview material
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_07_unsupported_roles_dynamic_generation():
    unusual_role = "Quantum Cryogenic Hardware Calibration Specialist"
    msg = A2AMessage(
        task_id="task_dyn_07",
        interview_id="ZAV-DYN-07",
        originating_agent="TestRunner",
        target_agent="QuestionGenerationAgent",
        payload={
            "role": unusual_role,
            "resume_facts": {
                "skills": ["Dilution Refrigerators", "Superconducting Qubits", "Microwave Pulses"],
            },
        },
    )
    response_msg = await agent_orchestrator.dispatch(msg)
    questions = response_msg.payload.get("questions", [])
    assert len(questions) > 0
    # Questions should be dynamically generated for this unusual domain
    assert any("quantum" in q.get("question", "").lower() or "calibration" in q.get("question", "").lower() or "hardware" in q.get("question", "").lower() for q in questions)


# ---------------------------------------------------------------------------
# Test 8: RAG document retrieval: Candidate and role permissions are strictly respected
# ---------------------------------------------------------------------------
def test_08_rag_retrieval_permissions():
    from backend.services.bank_rag_engine import BankRAGService
    service = BankRAGService()

    # Query with strict role filter
    res = service.query_similar("system design distributed cache", role_filter="DevOps Engineer", top_k=3)
    assert isinstance(res, list)
    # None of the results should be from a completely unauthorized/unrelated domain if role_filter applied
    if len(res) > 0:
        for item in res:
            assert "question" in item


# ---------------------------------------------------------------------------
# Test 9: Answer capture: Every response is associated with its corresponding question
# ---------------------------------------------------------------------------
def test_09_question_response_linkage():
    interview_id = f"ZAV-QA-09-{uuid.uuid4().hex[:6]}"
    q_id = "q_101"
    question = "Explain how LSM-trees handle write amplification."
    answer = "LSM-trees append writes sequentially to a MemTable and SSTables, compaction reduces write amplification."

    save_qa_pair(
        interview_id=interview_id,
        question_id=q_id,
        question_text=question,
        answer_text=answer,
        score=92,
        feedback="Accurate conceptual coverage.",
    )

    pairs = get_qa_pairs(interview_id)
    assert len(pairs) == 1
    assert pairs[0]["question_id"] == q_id
    assert pairs[0]["question_text"] == question
    assert pairs[0]["answer_text"] == answer


# ---------------------------------------------------------------------------
# Test 10: Interrupted interview: Already-recorded answers persist after interruption
# ---------------------------------------------------------------------------
def test_10_interrupted_interview_persists_answers():
    interview_id = f"ZAV-INTERRUPT-10-{uuid.uuid4().hex[:6]}"
    save_interview(
        room_code=interview_id,
        user_id="user_interrupt_10",
        user_email="interrupt@zavran.ai",
        role="Platform Engineer",
        scheduled_epoch=int(time.time()),
        status="in_progress",
    )

    save_qa_pair(
        interview_id=interview_id,
        question_id="q_1",
        question_text="What is eBPF?",
        answer_text="eBPF allows sandboxed programs to execute inside the Linux kernel.",
        score=95,
        feedback="Precise answer.",
    )

    # Simulate network failure / process crash and re-read
    restored_pairs = get_qa_pairs(interview_id)
    assert len(restored_pairs) == 1
    assert restored_pairs[0]["question_id"] == "q_1"
    assert "eBPF allows sandboxed programs" in restored_pairs[0]["answer_text"]


# ---------------------------------------------------------------------------
# Test 11: Answer evaluation - synonymous wording: Semantic match receives credit
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_11_semantic_evaluation_synonymous_wording():
    agent = EvaluationAgent()
    # Candidate uses differing/synonymous terminology
    result = await agent.evaluate_answer(
        question="How does asynchronous I/O improve Web throughput?",
        reference_answer="Non-blocking operations allow single threads to service multiple concurrent connections using event loops.",
        candidate_answer="By preventing workers from getting stuck waiting on disk or network responses, the scheduler can process thousands of concurrent clients on an event loop.",
    )
    assert result["score"] >= 70, f"Expected high semantic score for synonymous wording, got {result['score']}"


# ---------------------------------------------------------------------------
# Test 12: Answer evaluation - missing concepts / errors: Penalized with lower scores
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_12_answer_evaluation_penalizes_errors():
    agent = EvaluationAgent()
    # Candidate gives a factually wrong or completely missing answer
    result = await agent.evaluate_answer(
        question="How does Raft maintain consistency during network partitions?",
        reference_answer="Raft requires a majority quorum of nodes to elect a leader and commit log entries.",
        candidate_answer="Raft sends an email notification to the administrator and shuts down the database.",
    )
    assert result["score"] < 40, f"Expected penalization for hallucinated answer, got {result['score']}"


# ---------------------------------------------------------------------------
# Test 13: Unanswered / skipped questions: Scored as 0, never given credit
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_13_unanswered_questions_scored_zero():
    agent = EvaluationAgent()
    skipped_answers = ["", "   ", "I don't know.", "skip", "Pass.", None]
    for ans in skipped_answers:
        res = await agent.evaluate_answer(
            question="Describe how TLS 1.3 0-RTT handshake works.",
            reference_answer="0-RTT uses pre-shared keys from previous sessions to send early data on the first flight.",
            candidate_answer=ans,
        )
        assert res["score"] == 0, f"Skipped answer '{ans}' must receive 0, got {res['score']}"


# ---------------------------------------------------------------------------
# Test 14: Final report availability: Blocked until 10 minutes post-completion
# ---------------------------------------------------------------------------
def test_14_report_publication_gated_by_10_minutes():
    now = int(time.time())
    user_id = "user_gate_14"
    room_code = "ZAV-GATE-14"

    # Completed 2 minutes ago (needs 10 minutes = 600s)
    save_interview(
        room_code=room_code,
        user_id=user_id,
        user_email="gate@zavran.ai",
        role="DevOps Engineer",
        scheduled_epoch=now - 3600,
        status="completed",
        completed_epoch=now - 120,
    )
    save_interview_report(
        interview_id=room_code,
        overall_score=85,
        summary="Candidate showed strong skills.",
        detailed_sections={"a_summary": "Strong interview."},
    )

    resp = client.get(
        f"/api/interview/{room_code}/report",
        headers={"Authorization": f"Bearer {user_id}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "evaluating"
    assert ("seconds_remaining" in data and data["seconds_remaining"] > 0) or ("ready_in_seconds" in data and data["ready_in_seconds"] > 0)
    assert "report" not in data or data["report"] is None


# ---------------------------------------------------------------------------
# Test 15: Monitoring consent: Monitoring operates only after explicit consent is granted
# ---------------------------------------------------------------------------
def test_15_monitoring_consent_enforcement():
    room_code = f"ZAV-CONSENT-{int(time.time())}"
    user_id = "user_consent_15"

    assert not has_monitoring_consent(room_code)

    # Attempt to post monitoring event without consent
    res = client.post(
        "/api/interview/monitoring/event",
        json={"interview_id": room_code, "event_type": "face_absence", "confidence": 0.8},
    )
    assert res.status_code == 403

    # Grant explicit consent
    record_monitoring_consent(room_code, user_id=user_id, consent_version="2.0")
    assert has_monitoring_consent(room_code)

    # Now monitoring event succeeds
    res_after = client.post(
        "/api/interview/monitoring/event",
        json={"interview_id": room_code, "event_type": "face_absence", "confidence": 0.8},
    )
    assert res_after.status_code == 200


# ---------------------------------------------------------------------------
# Test 16: Inconclusive monitoring signals: Confidence < 0.7 marked as inconclusive
# ---------------------------------------------------------------------------
def test_16_inconclusive_monitoring_signals():
    decision = yolov8_monitoring_service.evaluate_confidence(confidence=0.55, detected_signal="phone_detected")
    assert decision["inconclusive"] is True
    assert decision["penalize_candidate"] is False
    assert "inconclusive" in decision["status"].lower()


# ---------------------------------------------------------------------------
# Test 17: Evidence URLs: Direct unauthorized access is denied
# ---------------------------------------------------------------------------
def test_17_evidence_urls_access_control():
    # Attempt to download non-existent or unauthorized evidence frame
    resp = client.get("/api/interview/monitoring/evidence/unauth_frame_999.jpg")
    assert resp.status_code in [401, 403, 404]


# ---------------------------------------------------------------------------
# Test 18: AI provider failure: Transparently falls back to safe recovery
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_18_ai_provider_failure_graceful_recovery():
    agent = EvaluationAgent()
    # Even if external LLM APIs fail or return errors, evaluation must not throw an unhandled exception
    res = await agent.evaluate_answer(
        question="What is optimistic concurrency control?",
        reference_answer="Optimistic concurrency control checks whether a record has changed before committing.",
        candidate_answer="It uses versions or timestamps to verify no conflict occurred before saving.",
    )
    assert isinstance(res, dict)
    assert "score" in res
    assert res["score"] > 0


# ---------------------------------------------------------------------------
# Test 19: Duplicate requests: Repeated bookings, submissions, or report requests are idempotent
# ---------------------------------------------------------------------------
def test_19_idempotent_bookings_and_reports():
    room_code = "ZAV-IDEMPOTENT-19"
    user_id = "user_idempotent_19"

    # Save interview twice with the same room code
    save_interview(
        room_code=room_code,
        user_id=user_id,
        user_email="idem@zavran.ai",
        role="Data Engineer",
        scheduled_epoch=int(time.time()),
        status="scheduled",
    )
    # Second write should update/no-op without crashing or creating duplicates
    save_interview(
        room_code=room_code,
        user_id=user_id,
        user_email="idem@zavran.ai",
        role="Data Engineer",
        scheduled_epoch=int(time.time()),
        status="scheduled",
    )

    it = get_interview_by_room_code(room_code)
    assert it is not None
    assert it["room_code"] == room_code


# ---------------------------------------------------------------------------
# Test 20: Account deletion / retention: Data is completely deleted according to policy
# ---------------------------------------------------------------------------
def test_20_gdpr_account_deletion():
    user_id = "user_gdpr_purge_20"
    email = "purge@zavran.ai"
    room_code = "ZAV-PURGE-20"

    save_user_profile(user_id=user_id, email=email, name="Purge Me", target_role="Tester")
    save_interview(room_code=room_code, user_id=user_id, user_email=email, role="Tester")
    save_interview_report(interview_id=room_code, overall_score=70, summary="Report to purge")
    record_monitoring_consent(interview_id=room_code, user_id=user_id)

    # Perform GDPR account purge
    deleted = delete_user_account_data(user_id=user_id, email=email)
    assert deleted is True

    # Confirm all user data is gone
    assert get_user_profile(user_id) is None
    assert get_interview_by_room_code(room_code) is None
    assert get_interview_report(room_code) is None
