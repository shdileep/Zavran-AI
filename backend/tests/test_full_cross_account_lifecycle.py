import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.interview_engine import interview_engine
from backend.providers.email_provider import EmailService, MockConsoleEmailProvider

class TestFullCrossAccountLifecycle(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_provider = MockConsoleEmailProvider()
        EmailService.set_provider(self.mock_provider)
        interview_engine.sessions.clear()
        interview_engine.user_interviews.clear()
        interview_engine.user_profiles.clear()
        interview_engine.user_dossiers.clear()
        interview_engine.email_delivery_logs.clear()

        self.account_a_id = 'usr_YWxpY2VAZXhhbXBsZS5jb20'
        self.account_b_id = 'usr_Ym9iQGV4YW1wbGUuY29t'
        self.headers_a = {'Authorization': f'Bearer {self.account_a_id}'}
        self.headers_b = {'Authorization': f'Bearer {self.account_b_id}'}

    def test_complete_cross_account_isolation_and_lifecycle(self):
        # STEP 1: Account A - Initial Login & Verification
        res_a_init = self.client.get('/api/user/interviews', headers=self.headers_a)
        self.assertEqual(res_a_init.status_code, 200)
        self.assertEqual(len(res_a_init.json().get('interviews', [])), 0, 'Account A must start with 0 interviews')

        stats_a_init = self.client.get('/api/user/dashboard-stats', headers=self.headers_a).json()['stats']
        self.assertEqual(stats_a_init['total_interviews'], 0)

        # Set Account A profile
        self.client.post(
            '/api/user/profile',
            headers=self.headers_a,
            json={'name': 'Alice Wonderland', 'email': 'alice@example.com', 'role': 'Principal AI Engineer'}
        )

        # STEP 2: Account A - Explicit Interview Scheduling
        sched_a = self.client.post(
            '/api/user/interviews/schedule',
            headers=self.headers_a,
            json={
                'room_code': 'ZAV-ALICE-101',
                'role': 'Principal AI Engineer',
                'company': 'Stripe',
                'interviewer': 'Zaroon',
                'date': '2026-09-20',
                'time': '10:00 AM – 10:30 AM',
                'candidate_name': 'Alice Wonderland'
            }
        )
        self.assertEqual(sched_a.status_code, 200)
        self.assertEqual(sched_a.json()['interview']['roomCode'], 'ZAV-ALICE-101')

        # Account A now has exactly 1 interview
        res_a_after = self.client.get('/api/user/interviews', headers=self.headers_a)
        interviews_a = res_a_after.json().get('interviews', [])
        self.assertEqual(len(interviews_a), 1)
        self.assertEqual(interviews_a[0]['roomCode'], 'ZAV-ALICE-101')
        self.assertEqual(interviews_a[0]['company'], 'Stripe')

        # STEP 3: Account B - Fresh Login & Isolation Check
        res_b_init = self.client.get('/api/user/interviews', headers=self.headers_b)
        self.assertEqual(res_b_init.status_code, 200)
        self.assertEqual(len(res_b_init.json().get('interviews', [])), 0, 'Account B must NEVER see Account A interviews')

        stats_b_init = self.client.get('/api/user/dashboard-stats', headers=self.headers_b).json()['stats']
        self.assertEqual(stats_b_init['total_interviews'], 0)

        prof_b_init = self.client.get('/api/user/profile', headers=self.headers_b).json()['profile']
        self.assertNotEqual(prof_b_init.get('name'), 'Alice Wonderland')

        # STEP 4: Account B - Security Checks on Account A resources
        get_sess_b = self.client.get('/api/interview/ZAV-ALICE-101/session', headers=self.headers_b)
        self.assertEqual(get_sess_b.status_code, 403, 'Account B must be forbidden from accessing Account A session')

        start_sess_b = self.client.post('/api/interview/ZAV-ALICE-101/start', headers=self.headers_b)
        self.assertEqual(start_sess_b.status_code, 403)

        ans_b = self.client.post(
            '/api/interview/ZAV-ALICE-101/submit-text-answer',
            headers=self.headers_b,
            json={'answer_text': 'Unauthorized answer attempt'}
        )
        self.assertEqual(ans_b.status_code, 403)

        cancel_b = self.client.post('/api/user/interviews/ZAV-ALICE-101/cancel', headers=self.headers_b)
        self.assertEqual(cancel_b.status_code, 404)

        del_b = self.client.delete('/api/user/interviews/ZAV-ALICE-101', headers=self.headers_b)
        self.assertEqual(del_b.status_code, 404)

        # STEP 5: Account B - Explicit Scheduling of its own Interview
        sched_b = self.client.post(
            '/api/user/interviews/schedule',
            headers=self.headers_b,
            json={
                'room_code': 'ZAV-BOB-202',
                'role': 'Security Systems Architect',
                'company': 'Databricks',
                'interviewer': 'Zaroon',
                'date': '2026-09-22',
                'time': '02:00 PM – 02:30 PM',
                'candidate_name': 'Bob Builder'
            }
        )
        self.assertEqual(sched_b.status_code, 200)

        # Account B has only its own interview
        res_b_final = self.client.get('/api/user/interviews', headers=self.headers_b)
        interviews_b = res_b_final.json().get('interviews', [])
        self.assertEqual(len(interviews_b), 1)
        self.assertEqual(interviews_b[0]['roomCode'], 'ZAV-BOB-202')
        self.assertEqual(interviews_b[0]['company'], 'Databricks')

        # Account A still has ONLY its own interview
        res_a_final = self.client.get('/api/user/interviews', headers=self.headers_a)
        interviews_a_final = res_a_final.json().get('interviews', [])
        self.assertEqual(len(interviews_a_final), 1)
        self.assertEqual(interviews_a_final[0]['roomCode'], 'ZAV-ALICE-101')
        self.assertEqual(interviews_a_final[0]['company'], 'Stripe')

if __name__ == '__main__':
    unittest.main()
