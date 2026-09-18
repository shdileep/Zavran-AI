import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.interview_engine import interview_engine, InterviewSession
from backend.providers.email_provider import EmailService, MockConsoleEmailProvider

class TestComprehensiveGuardrails(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_provider = MockConsoleEmailProvider()
        EmailService.set_provider(self.mock_provider)
        interview_engine.sessions.clear()
        interview_engine.user_interviews.clear()
        interview_engine.user_profiles.clear()
        interview_engine.user_dossiers.clear()
        interview_engine.email_delivery_logs.clear()

        self.user_a = 'usr_alice_tenant_A'
        self.user_b = 'usr_bob_tenant_B'
        self.headers_a = {'Authorization': f'Bearer {self.user_a}'}
        self.headers_b = {'Authorization': f'Bearer {self.user_b}'}

    def test_guardrail_1_tenant_isolation(self):
        # 1. Schedule for User A
        self.client.post('/api/user/interviews/schedule', headers=self.headers_a, json={
            'room_code': 'ZAV-GUARD-101', 'role': 'AI Researcher', 'company': 'DeepLab', 'candidate_name': 'Alice'
        })
        # User B cannot see User A interviews
        res_b = self.client.get('/api/user/interviews', headers=self.headers_b).json()
        self.assertEqual(len(res_b.get('interviews', [])), 0)

    def test_guardrail_2_auth_context_integrity(self):
        # Unauthenticated calls must be rejected with 401
        res = self.client.get('/api/user/interviews')
        self.assertEqual(res.status_code, 401)
        res_bad = self.client.get('/api/user/interviews', headers={'Authorization': 'Bearer bad-token-gibberish'})
        self.assertEqual(res_bad.status_code, 401)

    def test_guardrail_3_no_auto_room_creation(self):
        # Simply logging in, fetching profile, dashboard stats, or history must NOT create any room
        user_fresh = 'usr_fresh_login_user'
        h_fresh = {'Authorization': f'Bearer {user_fresh}'}
        self.client.get('/api/user/profile', headers=h_fresh)
        self.client.get('/api/user/dossier', headers=h_fresh)
        self.client.get('/api/user/dashboard-stats', headers=h_fresh)
        interviews = self.client.get('/api/user/interviews', headers=h_fresh).json().get('interviews', [])
        self.assertEqual(len(interviews), 0, 'No room must be auto-created on dashboard/profile load')
        self.assertEqual(len(interview_engine.sessions), 0, 'No session must exist in engine')

    def test_guardrail_4_resource_authorization(self):
        # Schedule for User A
        self.client.post('/api/user/interviews/schedule', headers=self.headers_a, json={
            'room_code': 'ZAV-AUTH-202', 'role': 'Security Lead', 'company': 'VaultCorp'
        })
        # User B cannot read session, start, submit, cancel, or delete User A interview
        self.assertEqual(self.client.get('/api/interview/ZAV-AUTH-202/session', headers=self.headers_b).status_code, 403)
        self.assertEqual(self.client.post('/api/interview/ZAV-AUTH-202/start', headers=self.headers_b).status_code, 403)
        self.assertEqual(self.client.post('/api/interview/ZAV-AUTH-202/submit-text-answer', headers=self.headers_b, json={'answer_text': 'hacked'}).status_code, 403)
        self.assertEqual(self.client.post('/api/user/interviews/ZAV-AUTH-202/cancel', headers=self.headers_b).status_code, 404)
        self.assertEqual(self.client.delete('/api/user/interviews/ZAV-AUTH-202', headers=self.headers_b).status_code, 404)

    def test_guardrail_5_state_machine_and_eval_integrity(self):
        # Scheduled interview starts as scheduled with no score
        res = self.client.post('/api/user/interviews/schedule', headers=self.headers_a, json={
            'room_code': 'ZAV-EVAL-303', 'role': 'MLOps Engineer', 'company': 'AutoML'
        }).json()
        interview = res['interview']
        self.assertEqual(interview['status'], 'scheduled')
        self.assertIsNone(interview['score'])

        # Start interview -> in_progress
        start_res = self.client.post('/api/interview/ZAV-EVAL-303/start', headers=self.headers_a)
        self.assertEqual(start_res.status_code, 200)
        self.assertEqual(start_res.json()['session']['status'], 'in_progress')

        # List interviews shows in_progress
        list_res = self.client.get('/api/user/interviews', headers=self.headers_a).json()['interviews']
        self.assertEqual(list_res[0]['status'], 'in_progress')

    def test_guardrail_6_idempotent_scheduling(self):
        # Rescheduling the same room code updates the record instead of duplicating
        self.client.post('/api/user/interviews/schedule', headers=self.headers_a, json={
            'room_code': 'ZAV-IDEMPOTENT-1', 'role': 'Role V1', 'company': 'Company 1'
        })
        self.client.post('/api/user/interviews/schedule', headers=self.headers_a, json={
            'room_code': 'ZAV-IDEMPOTENT-1', 'role': 'Role V2', 'company': 'Company 2'
        })
        interviews = self.client.get('/api/user/interviews', headers=self.headers_a).json()['interviews']
        self.assertEqual(len(interviews), 1, 'Must not duplicate interview records with same room code')
        self.assertEqual(interviews[0]['role'], 'Role V2')

    def test_guardrail_7_profile_dossier_data_isolation(self):
        self.client.post('/api/user/profile', headers=self.headers_a, json={'name': 'Alice A', 'email': 'alice@a.com'})
        self.client.post('/api/user/profile', headers=self.headers_b, json={'name': 'Bob B', 'email': 'bob@b.com'})

        prof_a = self.client.get('/api/user/profile', headers=self.headers_a).json()['profile']
        prof_b = self.client.get('/api/user/profile', headers=self.headers_b).json()['profile']
        self.assertEqual(prof_a['name'], 'Alice A')
        self.assertEqual(prof_b['name'], 'Bob B')

if __name__ == '__main__':
    unittest.main()
