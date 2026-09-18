import asyncio
import unittest
import json
import time
from unittest.mock import patch, MagicMock
from backend.clerk_auth import ClerkAuth
from backend.providers.email_provider import (
    EmailService,
    MockConsoleEmailProvider,
)
from backend.interview_engine import InterviewSession, InterviewEngine
from backend.config import settings

class TestClerkAuthEmailResolution(unittest.TestCase):
    def test_extract_verified_primary_email(self):
        user_obj = {
            "id": "user_123",
            "primary_email_address_id": "email_abc",
            "email_addresses": [
                {
                    "id": "email_xyz",
                    "email_address": "secondary@example.com",
                    "verification": {"status": "verified"}
                },
                {
                    "id": "email_abc",
                    "email_address": "primary.verified@example.com",
                    "verification": {"status": "verified"}
                }
            ]
        }
        email = ClerkAuth.extract_verified_email_from_user_obj(user_obj)
        self.assertEqual(email, "primary.verified@example.com")

    def test_fallback_to_any_verified_email_if_primary_unverified(self):
        user_obj = {
            "id": "user_456",
            "primary_email_address_id": "email_unverified",
            "email_addresses": [
                {
                    "id": "email_unverified",
                    "email_address": "unverified@example.com",
                    "verification": {"status": "unverified"}
                },
                {
                    "id": "email_valid",
                    "email_address": "fallback.verified@example.com",
                    "verification": {"status": "verified"}
                }
            ]
        }
        email = ClerkAuth.extract_verified_email_from_user_obj(user_obj)
        self.assertEqual(email, "fallback.verified@example.com")

    def test_extract_empty_when_no_user(self):
        self.assertIsNone(ClerkAuth.extract_verified_email_from_user_obj(None))
        self.assertIsNone(ClerkAuth.extract_verified_email_from_user_obj({}))


class TestEmailContentAndSecuritySanitization(unittest.TestCase):
    def setUp(self):
        self.sample_report = {
            "candidate": "Alex Rivera",
            "role": "Staff Distributed Systems Engineer",
            "org": "HyperScale Labs",
            "interviewer": "Zaroon AI",
            "overall_score": 92,
            "status": "Qualified — Recommended for Hire",
            "summary": "Demonstrated profound mastery of streaming low-latency architectures.",
            "greeting": "Hello Alex Rivera, thank you for interviewing for Staff Distributed Systems Engineer.",
            "strengths": [
                {
                    "title": "Low Latency Systems",
                    "what": "Clear understanding of SSE and WebSockets.",
                    "where": "Question 1",
                    "why": "Explained backpressure handling effectively."
                }
            ],
            "areas_for_improvement": [
                {
                    "title": "Edge Quantization",
                    "observed_weakness": "Did not elaborate on INT4 vs FP8 trade-offs.",
                    "question_context": "Question 3",
                    "missing_concepts": ["AWQ", "GPTQ"],
                    "concrete_improvement": "Review quantization hardware requirements."
                }
            ],
            "topic_performance": [
                {
                    "topic": "Streaming AI Pipelines",
                    "category": "Architecture",
                    "score": 94,
                    "evaluator_feedback": "Excellent streaming intuition.",
                    "concepts_covered": ["SSE", "Caching"],
                    "concepts_missed": []
                }
            ],
            "depth_analysis": {
                "overall_depth_level": 4,
                "depth_title": "Level 4 — Systems Architect",
                "rationale": "Articulates deep trade-offs across storage, memory, and networking."
            },
            "recommended_focus_areas": ["Advanced Quantization Caching"],
            # Secret keys that should NEVER leak
            "internal_hidden_rubric": {"unacceptable_misconceptions": ["Should not be in email"]},
            "system_prompt": "You are a harsh evaluator with secret rubrics.",
        }

    def test_email_content_contains_candidate_details(self):
        content = EmailService.generate_report_email_content(
            candidate_name="Alex Rivera",
            report_id="TEST-SESSION-999",
            report=self.sample_report,
        )
        html = content["html"]
        text = content["text"]
        subject = content["subject"]

        self.assertIn("Feedback Report", subject)
        self.assertIn("92/100", text)
        self.assertIn("92", html)
        self.assertIn("/100", html)
        self.assertIn("Alex Rivera", html)
        self.assertIn("Staff Distributed Systems Engineer", html)
        self.assertIn("interview-report/TEST-SESSION-999", html)

        # Security check: Internal hidden rubrics and system prompts are NOT exposed in email
        self.assertNotIn("internal_hidden_rubric", html)
        self.assertNotIn("You are a harsh evaluator", html)
        if settings.SMALLEST_API_KEY:
            self.assertNotIn(settings.SMALLEST_API_KEY, html)


class TestEmailDispatchAndDuplicateProtection(unittest.IsolatedAsyncioTestCase):
    async def test_duplicate_protection_idempotency(self):
        engine = InterviewEngine()
        session = InterviewSession(
            interview_id="IDEMPOTENT-TEST-1",
            candidate_name="Jane Doe",
            target_role="AI Engineer",
            org_name="TechCorp"
        )
        session.clerk_user_id = "user_test_jane"
        session.clerk_verified_email = "jane.doe@example.com"
        session.final_report = {
            "candidate": "Jane Doe",
            "role": "AI Engineer",
            "org": "TechCorp",
            "overall_score": 90,
            "status": "Qualified"
        }

        # Mock EmailService.send_candidate_report_email
        with patch.object(EmailService, "send_candidate_report_email", return_value={"success": True, "provider": "mock", "recipient": "jane.doe@example.com"}) as mock_send:
            # First send
            res1 = await engine._dispatch_report_email(session)
            self.assertTrue(res1.get("success"))
            self.assertTrue(session.email_sent)
            self.assertEqual(session.report_status, "EMAIL_SENT")
            self.assertIsNotNone(session.emailed_at)
            self.assertEqual(mock_send.call_count, 1)

            # Second send (Duplicate prevention)
            res2 = await engine._dispatch_report_email(session)
            self.assertTrue(res2.get("success"))
            self.assertEqual(res2.get("message"), "Email already sent")
            # EmailService should NOT be called again
            self.assertEqual(mock_send.call_count, 1)

    async def test_failure_handling_and_retry_without_re_evaluation(self):
        engine = InterviewEngine()
        session = InterviewSession(
            interview_id="RETRY-TEST-1",
            candidate_name="Bob Smith",
            target_role="Backend Engineer",
            org_name="CloudOrg"
        )
        session.clerk_user_id = "user_test_bob"
        session.clerk_verified_email = "bob@example.com"
        session.final_report = {
            "candidate": "Bob Smith",
            "role": "Backend Engineer",
            "org": "CloudOrg",
            "overall_score": 85,
            "status": "Qualified"
        }

        # Simulate network error on first email dispatch attempt
        with patch.object(EmailService, "send_candidate_report_email", return_value={"success": False, "error": "SMTP Connection Timeout"}):
            res_fail = await engine._dispatch_report_email(session)
            self.assertFalse(res_fail.get("success"))
            self.assertFalse(session.email_sent)
            self.assertEqual(session.report_status, "EMAIL_FAILED")
            self.assertEqual(session.email_error, "SMTP Connection Timeout")
            # Report remains intact
            self.assertIsNotNone(session.final_report)

        # Retry email delivery without re-evaluating LLM
        with patch.object(EmailService, "send_candidate_report_email", return_value={"success": True, "provider": "mock", "recipient": "bob@example.com"}):
            res_retry = await engine.retry_email_delivery(session)
            self.assertTrue(res_retry.get("success"))
            self.assertTrue(session.email_sent)
            self.assertEqual(session.report_status, "EMAIL_SENT")
            self.assertIsNone(session.email_error)


if __name__ == "__main__":
    unittest.main()
