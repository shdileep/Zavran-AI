from unittest.mock import patch, AsyncMock
import unittest
import json
from fastapi.testclient import TestClient
from backend.main import app
from backend.interview_engine import interview_engine, InterviewSession
from backend.providers.email_provider import EmailService, MockConsoleEmailProvider

class TestSecurityAccountIsolation(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_provider = MockConsoleEmailProvider()
        EmailService.set_provider(self.mock_provider)
        interview_engine.sessions.clear()
        interview_engine.user_interviews.clear()
        interview_engine.user_profiles.clear()
        interview_engine.user_dossiers.clear()
        interview_engine.email_delivery_logs.clear()

        self.user_a_token = "user_alice_111"
        self.user_b_token = "user_bob_222"
        self.headers_a = {"Authorization": f"Bearer {self.user_a_token}"}
        self.headers_b = {"Authorization": f"Bearer {self.user_b_token}"}

    def test_account_isolation_and_scheduling(self):
        res_a = self.client.post(
            "/api/user/interviews/schedule",
            headers=self.headers_a,
            json={
                "room_code": "ZAV-ALICE-99",
                "role": "Lead Distributed AI Architect",
                "company": "ScaleTech Inc",
                "candidate_name": "Alice Developer"
            }
        )
        self.assertEqual(res_a.status_code, 200)
        self.assertTrue(res_a.json().get("success"))

        list_a = self.client.get("/api/user/interviews", headers=self.headers_a)
        self.assertEqual(list_a.status_code, 200)
        interviews_a = list_a.json().get("interviews", [])
        self.assertEqual(len(interviews_a), 1)
        self.assertEqual(interviews_a[0]["roomCode"], "ZAV-ALICE-99")

        list_b = self.client.get("/api/user/interviews", headers=self.headers_b)
        self.assertEqual(list_b.status_code, 200)
        interviews_b = list_b.json().get("interviews", [])
        self.assertEqual(len(interviews_b), 0, "User B must NEVER see User A scheduled interview")

    @patch("backend.interview_engine.interview_engine.prepare_interview_plan")
    def test_resource_level_authorization(self, mock_prep):
        session = interview_engine.get_or_create_session(
            interview_id="ZAV-ALICE-SECRET",
            candidate_name="Alice",
            target_role="Staff Engineer",
            org_name="ScaleTech"
        )
        session.clerk_user_id = self.user_a_token
        mock_prep.return_value = session.get_candidate_safe_state()

        res_prep = self.client.post(
            "/api/interview/prepare",
            headers=self.headers_a,
            json={
                "interview_id": "ZAV-ALICE-SECRET",
                "candidate_name": "Alice",
                "target_role": "Staff Engineer",
                "resume_text": "Alice Resume Content",
                "jd_text": "Staff Engineer Job Description"
            }
        )
        self.assertEqual(res_prep.status_code, 200)

        res_get_a = self.client.get("/api/interview/ZAV-ALICE-SECRET/session", headers=self.headers_a)
        self.assertEqual(res_get_a.status_code, 200)

        res_get_b = self.client.get("/api/interview/ZAV-ALICE-SECRET/session", headers=self.headers_b)
        self.assertEqual(res_get_b.status_code, 403)

        res_start_b = self.client.post("/api/interview/ZAV-ALICE-SECRET/start", headers=self.headers_b)
        self.assertEqual(res_start_b.status_code, 403)

        res_sub_b = self.client.post(
            "/api/interview/ZAV-ALICE-SECRET/submit-text-answer",
            headers=self.headers_b,
            json={"answer_text": "I am an attacker trying to submit on Alice interview"}
        )
        self.assertEqual(res_sub_b.status_code, 403)

        res_rep_b = self.client.get("/api/interview/ZAV-ALICE-SECRET/report", headers=self.headers_b)
        self.assertEqual(res_rep_b.status_code, 403)

        res_del_b = self.client.delete("/api/user/interviews/ZAV-ALICE-SECRET", headers=self.headers_b)
        self.assertIn(res_del_b.status_code, [403, 404])

    def test_unauthenticated_request_rejected(self):
        self.client.post(
            "/api/user/interviews/schedule",
            headers=self.headers_a,
            json={
                "room_code": "ZAV-ALICE-SECURE",
                "role": "Backend Engineer",
                "company": "CloudCorp"
            }
        )

        res_no_auth_session = self.client.get("/api/interview/ZAV-ALICE-SECURE/session")
        self.assertEqual(res_no_auth_session.status_code, 401)

        res_no_auth_interviews = self.client.get("/api/user/interviews")
        self.assertEqual(res_no_auth_interviews.status_code, 401)

        res_invalid_auth = self.client.get(
            "/api/user/interviews",
            headers={"Authorization": "Bearer invalid_gibberish_token"}
        )
        self.assertEqual(res_invalid_auth.status_code, 401)

    def test_user_profile_and_dossier_isolation(self):
        self.client.post(
            "/api/user/profile",
            headers=self.headers_a,
            json={"name": "Alice Smith", "role": "Lead AI Architect", "email": "alice@scale.com"}
        )

        self.client.post(
            "/api/user/profile",
            headers=self.headers_b,
            json={"name": "Bob Jones", "role": "Security Researcher", "email": "bob@defense.com"}
        )

        prof_a = self.client.get("/api/user/profile", headers=self.headers_a).json().get("profile")
        self.assertEqual(prof_a.get("name"), "Alice Smith")
        self.assertEqual(prof_a.get("role"), "Lead AI Architect")

        prof_b = self.client.get("/api/user/profile", headers=self.headers_b).json().get("profile")
        self.assertEqual(prof_b.get("name"), "Bob Jones")
        self.assertEqual(prof_b.get("role"), "Security Researcher")

    def test_no_automatic_interview_creation_on_login(self):
        # When a new user logs in and queries profile and dashboard stats, interviews must be exactly empty
        user_c_token = "user_charlie_333"
        headers_c = {"Authorization": f"Bearer {user_c_token}"}

        prof_res = self.client.get("/api/user/profile", headers=headers_c)
        self.assertEqual(prof_res.status_code, 200)

        stats_res = self.client.get("/api/user/dashboard-stats", headers=headers_c)
        self.assertEqual(stats_res.status_code, 200)
        self.assertEqual(stats_res.json()["stats"]["total_interviews"], 0)

        interviews_res = self.client.get("/api/user/interviews", headers=headers_c)
        self.assertEqual(interviews_res.status_code, 200)
        self.assertEqual(len(interviews_res.json()["interviews"]), 0, "New user must have 0 interviews")

    def test_admin_email_test_endpoint_and_tracking(self):
        res = self.client.post(
            "/api/admin/email/test",
            headers=self.headers_a,
            json={
                "recipient_email": "alice.verified@example.com",
                "subject": "Admin Delivery Check",
                "message": "Testing delivery pipeline"
            }
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("recipient"), "alice.verified@example.com")
        self.assertEqual(data.get("status"), "accepted")

        self.assertGreater(len(interview_engine.email_delivery_logs), 0)
        last_log = interview_engine.email_delivery_logs[-1]
        self.assertEqual(last_log["recipient"], "alice.verified@example.com")
        self.assertEqual(last_log["user_id"], self.user_a_token)
        self.assertEqual(last_log["status"], "ACCEPTED_BY_PROVIDER")

if __name__ == "__main__":
    unittest.main()
