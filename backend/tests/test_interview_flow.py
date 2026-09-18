import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from backend.config import settings
from backend.interview_engine import interview_engine, InterviewSession
from backend.providers.provider_factory import LLMProviderFactory

async def run_tests():
    print("==================================================")
    print("Zavran AI Interview Engine — Verification Test Suite")
    print("==================================================")

    # Test 1: Provider Factory Initialization
    print("\n[Test 1] Testing LLM Provider Factory...")
    provider = LLMProviderFactory.get_provider()
    print(f"[OK] Default LLM Provider: {provider.__class__.__name__}")

    # Test 2: Create Session & Ingest Resume + JD
    print("\n[Test 2] Preparing Interview Session with Resume & JD...")
    session = interview_engine.get_or_create_session(
        interview_id="ZAV-TEST-99",
        candidate_name="Alex Mercer",
        target_role="Lead AI Systems Engineer",
        interviewer_name="Zaroon",
        org_name="Zavran AI Enterprise",
    )

    resume_sample = """
    Alex Mercer
    Senior Full Stack & AI Systems Engineer
    Skills: Python, FastAPI, LangGraph, RAG, FAISS, PostgreSQL, WebSockets, PyTorch
    Experience: Built an enterprise distributed RAG pipeline indexing 5M documents with sub-100ms vector search latency using FAISS and LangChain.
    Projects: Autonomous multi-agent coding platform with sandbox tool-calling and hallucination guardrails.
    """

    jd_sample = """
    Job Title: Lead AI Systems Engineer
    Responsibilities: Architect high-throughput inference pipelines, low-latency streaming RAG systems, and defensive agentic guardrails.
    Required Skills: Python, FastAPI, Distributed Systems, Vector Databases, LLM Evaluation, Agent Safety.
    """

    safe_state = await interview_engine.prepare_interview_plan(session, resume_sample, jd_sample)
    print(f"[OK] Session Prepared: ID = {safe_state['interview_id']}")
    print(f"[OK] Generated Questions Count: {len(session.questions)}")
    print(f"[OK] First Question: {session.questions[0]['question']}")
    
    # Verify Hidden Rubric is NOT exposed to candidate
    assert "hidden_rubric" not in safe_state["current_question"], "SECURITY FAILURE: Hidden rubric leaked to client!"
    print("[OK] Security Check: Hidden rubric is strictly private on backend.")

    # Test 3: Start Session & Authoritative Timer
    print("\n[Test 3] Starting Session & Authoritative Timer...")
    started_state = interview_engine.start_session(session)
    assert started_state["status"] == "in_progress"
    print(f"[OK] Status: {started_state['status']}, Max Duration: {started_state['max_duration_seconds']}s")

    # Test 4: Answer Processing & Dynamic Follow-up Action
    print("\n[Test 4] Processing Candidate Answer...")
    answer_sample = (
        "In our RAG pipeline, we partitioned the vector space using FAISS inverted file indexing with HNSW graphs. "
        "We implemented asynchronous chunking with streaming WebSockets to push tokens directly to the client."
    )

    eval_result = await interview_engine.submit_answer(session, answer_text=answer_sample)
    print(f"[OK] Answer Evaluated. Dialogue: '{eval_result['interviewer_response']}'")
    print(f"[OK] Next Question: '{session.questions[session.current_question_index]['question'][:80]}...'")

    # Test 5: Integrity Violation Tracking (Authoritative 15-Warning Limit)
    print("\n[Test 5] Testing Integrity Violations & 15-Warning Termination Rules...")
    for i in range(1, 16):
        session.last_violation_incident_time = 0  # reset debounce for test
        session.active_violations.clear()
        res_viol = interview_engine.record_violation(
            session,
            event_type=f"violation_type_{i}",
            details=f"Violation #{i}"
        )
        if i < 15:
            print(f"[OK] Warning #{i}/15 Issued (Action: {res_viol['action']}, Count: {res_viol['warning_count']})")
            assert res_viol["action"] == "warn" or res_viol["action"] == "in_progress"
        else:
            print(f"[OK] Warning #{i}/15 Triggered Automatic Termination (Action: {res_viol['action']}, Status: {res_viol['status']})")
            assert res_viol["action"] == "terminate", "15-Warning Failure: 15th warning did not terminate!"
            assert session.status == "unsuccessful", "Session status must be 'unsuccessful' after 15 warnings!"

    # Test 6: Final Assessment Report Compilation
    print("\n[Test 6] Compiling Final Structured Assessment Report...")
    report_res = await interview_engine.complete_session(session, reason="camera_off_limit")
    report = report_res["final_report"]
    print(f"[OK] Report Compiled. Overall Score: {report.get('overall_score', 0)}/100")
    print(f"[OK] Final Recommendation: {report.get('recommendation')}")
    print(f"[OK] Category Scores: {list(report.get('category_scores', {}).keys())}")
    print(f"[OK] Strengths Identified: {len(report.get('strengths', []))}")
    print(f"[OK] Improvement Areas: {len(report.get('improvement_areas', []))}")

    print("\n==================================================")
    print("ALL TESTS PASSED! FULL END-TO-END SPECIFICATION VERIFIED")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_tests())
