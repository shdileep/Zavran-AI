import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from backend.config import settings
from backend.interview_engine import interview_engine, InterviewSession
from backend.providers.provider_factory import LLMProviderFactory

async def run_memory_and_evaluation_tests():
    print("========================================================")
    print("ZAVRAN AI — FULL INTERVIEW MEMORY & EVALUATION TEST SUITE")
    print("========================================================")

    # 1. Create Session with full metadata
    session = interview_engine.get_or_create_session(
        interview_id="ZAV-MEM-TEST-01",
        candidate_name="Devon Archer",
        target_role="Principal AI Architect",
        interviewer_name="Zaroon AI",
        org_name="HyperScale Labs",
    )

    print("\n[1] Initializing Session & Memory Structures...")
    assert len(session.questions) >= 3
    for q in session.questions:
        assert "expected_answer_model" in q, f"Question {q['id']} missing expected_answer_model"
        assert "critical_concepts" in q["expected_answer_model"]
        assert "important_concepts" in q["expected_answer_model"]
        assert "unacceptable_misconceptions" in q["expected_answer_model"]
    print("[OK] Structured ExpectedAnswerModel confirmed on all questions.")

    # 2. Start session
    interview_engine.start_session(session)
    assert session.status == "in_progress"

    # 3. Simulate multi-turn question answering
    answers = [
        "To architect low-latency AI streaming pipelines, we decouple token generation from downstream consumers using Server-Sent Events over HTTP/2. We implement semantic caching in Redis and chunk embeddings with FAISS vector search to reduce context window load.",
        "For production tool-calling agents, we enforce Pydantic schemas on all function arguments, run all tool actions in ephemeral sandboxes with least-privilege tokens, and utilize validation retry loops with deterministic error payloads.",
        "Evaluating frontier APIs vs self-hosted open-source models requires token unit economics versus GPU infrastructure amortization. We fine-tune AWQ quantized 70B models for domain tasks while keeping frontier APIs for open-domain reasoning."
    ]

    print("\n[2] Processing Multi-turn Answers with Memory Retention...")
    for idx, ans in enumerate(answers):
        res = await interview_engine.process_candidate_response(session, speech_text=ans, duration_seconds=42.0)
        print(f"   -> Answered Question {idx+1}: Status = {res['status']}, Acknowledgement = \"{res['acknowledgement']}\"")

    # Verify structured memory stores
    assert len(session.answers) == 3, f"Expected 3 answers in memory, got {len(session.answers)}"
    assert len(session.evaluation_events) == 3, f"Expected 3 evaluation events, got {len(session.evaluation_events)}"

    print("\n[3] Verifying Stored Evaluation Memory Fields...")
    for ev in session.evaluation_events:
        print(f"   -> Event for {ev['question_id']}: Depth Level {ev['depth_level']}, Covered Concepts: {ev['concepts_covered']}")
        assert ev["depth_level"] in [1, 2, 3, 4, 5]
        assert len(ev["concepts_covered"]) > 0

    # 4. Test Cross-Question Consistency Provider
    print("\n[4] Testing Cross-Question Consistency & Depth Progression...")
    cross_res = await LLMProviderFactory.execute_with_fallback(
        "analyze_cross_question_consistency",
        session.questions,
        session.answers,
        session.evaluations,
    )
    print(f"   -> Contradictions Detected: {len(cross_res.get('contradictions_detected', []))}")
    print(f"   -> Progression Rationale: {cross_res.get('depth_progression', '')[:80]}...")
    assert "overall_consistency_score" in cross_res

    # 5. Execute Multi-stage Async Evaluation Pipeline
    print("\n[5] Executing Multi-Stage Asynchronous Evaluation Pipeline...")
    report = await interview_engine.evaluate_full_interview_session(session, reason="completed")
    
    assert session.evaluation_stage == "ready"
    assert session.evaluation_progress == 100
    assert report is not None

    print(f"   -> Candidate Greeting: {report.get('greeting')}")
    print(f"   -> Overall Rigor Score: {report.get('overall_score')}/100")
    print(f"   -> Strengths Count (WHAT+WHERE+WHY): {len(report.get('strengths', []))}")
    for st in report.get("strengths", []):
        assert "what" in st and "where" in st and "why" in st, f"Strength missing WHAT/WHERE/WHY: {st}"
        print(f"      * Strength: {st['title']} [WHERE: {st['where']}]")

    print(f"   -> Areas for Improvement: {len(report.get('areas_for_improvement', []))}")
    for imp in report.get("areas_for_improvement", []):
        assert "observed_weakness" in imp and "question_context" in imp and "concrete_improvement" in imp
        print(f"      * Weakness: {imp['title']} [Context: {imp['question_context']}]")

    print(f"   -> Topic Categories Performance: {len(report.get('topic_performance', []))}")
    for tp in report.get("topic_performance", []):
        assert "topic" in tp and "score" in tp and "concepts_covered" in tp
        print(f"      * Topic: {tp['topic']} -> Score: {tp['score']}")

    print(f"   -> Internal Audit Table Rows: {len(report.get('internal_audit_table', []))}")
    assert len(report.get("internal_audit_table", [])) == 3
    for audit in report.get("internal_audit_table", []):
        assert "raw_candidate_answer" in audit
        assert "expected_concepts" in audit
        assert "covered_concepts" in audit
        print(f"      * Audit Q: {audit['question_id']} -> Depth: {audit['depth_level']}")

    print("\n========================================================")
    print("ALL FULL INTERVIEW MEMORY & EVALUATION TESTS PASSED (100%)")
    print("========================================================")

if __name__ == "__main__":
    asyncio.run(run_memory_and_evaluation_tests())

