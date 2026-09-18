import unittest
import asyncio
from backend.interview_engine import InterviewEngine, InterviewSession
from backend.providers.provider_factory import LLMProviderFactory, HeuristicFallbackProvider
from backend.providers.email_provider import EmailService

class TestModelTrainingAndTimers(unittest.TestCase):
    def setUp(self):
        self.engine = InterviewEngine()
        self.provider = HeuristicFallbackProvider()

    def test_20_question_generation_structure(self):
        """Verify that generate_interview_plan generates exactly 20 structured questions with correct category distributions."""
        candidate_profile = {
            "name": "Alex Mercer",
            "skills": ["Python", "FastAPI", "React", "PostgreSQL", "LangGraph"],
            "projects": [{"title": "Autonomous Multi-Agent Platform", "technologies": ["LangGraph", "FastAPI"]}],
            "experience": [{"company": "AI Enterprise", "role": "Senior Engineer"}]
        }
        jd_profile = {
            "job_title": "Principal AI Platform Engineer",
            "required_skills": ["Python", "FastAPI", "Distributed Systems", "Vector Databases", "LLM Evaluation"],
            "preferred_skills": ["LangGraph", "WebSockets"],
            "domain": "Artificial Intelligence & Enterprise Systems"
        }
        
        loop = asyncio.new_event_loop()
        questions = loop.run_until_complete(
            self.provider.generate_interview_plan(
                candidate_profile=candidate_profile,
                jd_profile=jd_profile
            )
        )
        loop.close()

        self.assertEqual(len(questions), 20, f"Expected 20 questions, got {len(questions)}")
        
        # Check first 3 are resume depth
        for q in questions[:3]:
            self.assertEqual(q.get("source"), "resume")
            concepts = q.get("concepts_tested") or q.get("expected_concepts") or q.get("expected_answer_model", {}).get("critical_concepts", [])
            self.assertTrue(len(concepts) > 0)

        # Check Q4-Q10 are resume_jd_mixed
        for q in questions[3:10]:
            self.assertIn(q.get("source"), ["resume_jd", "resume_jd_mixed"])

        # Check Q11-Q20 are pure_jd_role_fit
        for q in questions[10:]:
            self.assertIn(q.get("source"), ["pure_jd_role_fit", "jd"])

    def test_exact_answer_memory_retention(self):
        """Verify that candidate answers are preserved verbatim in candidate_answer_raw and transcript."""
        session = self.engine.get_or_create_session(
            interview_id="TEST-EXACT-MEM-1",
            candidate_name="Jane Doe",
            target_role="Full Stack AI Engineer"
        )
        
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.engine.prepare_interview_plan(session, "Python, React developer", "Build AI agents"))
        
        raw_answer = "We implement token streaming over Server-Sent Events with Redis caching and structured Pydantic schema validation."
        resp = loop.run_until_complete(
            self.engine.process_candidate_response(
                session=session,
                speech_text=raw_answer,
                duration_seconds=12.5
            )
        )
        loop.close()

        self.assertTrue(len(session.answers) > 0)
        saved_record = session.answers[0]
        self.assertEqual(saved_record["candidate_answer_raw"], raw_answer)
        self.assertEqual(saved_record["candidate_answer_transcript"], raw_answer)
        self.assertIn("concepts_detected", saved_record)
        self.assertIn("depth", saved_record)
        self.assertFalse(saved_record.get("skip_detected", False))

    def test_skip_intent_and_adaptive_transition_delay(self):
        """Verify that semantic skip phrases trigger skip_detected=True and transition_delay_ms=2000."""
        session = self.engine.get_or_create_session(
            interview_id="TEST-SKIP-1",
            candidate_name="Jane Doe",
            target_role="Full Stack AI Engineer"
        )
        
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.engine.prepare_interview_plan(session, "Python developer", "Build AI agents"))
        
        skip_speech = "I don't know the answer to this, can we please skip to the next question?"
        resp = loop.run_until_complete(
            self.engine.process_candidate_response(
                session=session,
                speech_text=skip_speech,
                duration_seconds=2.0
            )
        )
        loop.close()

        self.assertTrue(resp.get("skip_detected"))
        self.assertEqual(resp.get("transition_delay_ms"), 2000)
        self.assertIn("Alright, let's move to the next one", resp.get("acknowledgement"))

    def test_ready_email_duplicate_protection_and_table(self):
        """Verify that interview ready email contains all required tabular fields and duplicate prevention."""
        session = self.engine.get_or_create_session(
            interview_id="TEST-READY-EMAIL-1",
            candidate_name="Bob Builder",
            target_role="Cloud Architect",
            org_name="Acme Corp"
        )
        session.clerk_verified_email = "bob@example.com"

        content = EmailService.generate_interview_ready_email_content(
            candidate_name="Bob Builder",
            company="Acme Corp",
            role="Cloud Architect",
            organization="Acme Corp",
            interviewer_name="Zaroon",
            interview_date="October 25, 2026",
            interview_time="10:00 AM UTC",
            room_code="TEST-READY-EMAIL-1"
        )

        self.assertIn("Acme Corp", content["html"])
        self.assertIn("Cloud Architect", content["html"])
        self.assertIn("TEST-READY-EMAIL-1", content["html"])
        self.assertIn("table", content["html"].lower())

        loop = asyncio.new_event_loop()
        res1 = loop.run_until_complete(
            self.engine.send_room_ready_email(
                session=session,
                company="Acme Corp",
                role="Cloud Architect",
                organization="Acme Corp",
                interviewer_name="Zaroon",
                interview_date="October 25, 2026",
                interview_time="10:00 AM UTC"
            )
        )
        self.assertTrue(res1["success"])
        self.assertTrue(session.ready_email_sent)

        # Second call should be prevented (idempotent)
        res2 = loop.run_until_complete(
            self.engine.send_room_ready_email(
                session=session,
                company="Acme Corp",
                role="Cloud Architect",
                organization="Acme Corp",
                interviewer_name="Zaroon",
                interview_date="October 25, 2026",
                interview_time="10:00 AM UTC"
            )
        )
        loop.close()

        self.assertTrue(res2["success"])
        self.assertTrue(res2.get("duplicate_prevented", False))

    def test_30_minute_authoritative_session_duration(self):
        """Verify that interview session enforces max 30-minute duration."""
        session = self.engine.get_or_create_session(interview_id="TEST-DURATION-1")
        self.assertEqual(session.max_duration_seconds, 30 * 60)

if __name__ == "__main__":
    unittest.main()
