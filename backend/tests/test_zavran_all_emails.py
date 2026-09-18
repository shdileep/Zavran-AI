import unittest
import asyncio
from backend.config import settings
from backend.providers.email_provider import (
    EmailService,
    MockConsoleEmailProvider,
    get_logo_base64,
    get_default_from_email,
)
from backend.interview_engine import interview_engine, InterviewSession
from fastapi.testclient import TestClient
from backend.main import app

class TestZavranAllEmails(unittest.TestCase):
    def setUp(self):
        self.mock_provider = MockConsoleEmailProvider()
        EmailService.set_provider(self.mock_provider)
        self.client = TestClient(app)

    def test_default_sender_and_logo(self):
        self.assertEqual(get_default_from_email(), 'support.zarvanai@gmail.com')
        logo_b64 = get_logo_base64()
        self.assertTrue(len(logo_b64) > 100, 'Logo base64 must be loaded from zevaro.png')

    def test_1_welcome_email_generation_and_dispatch(self):
        async def run():
            res = await EmailService.send_welcome_email(
                to_email='candidate@example.com',
                candidate_name='Alex Mercer',
            )
            self.assertTrue(res.get('success'))
            self.assertEqual(len(self.mock_provider.sent_emails), 1)
            last = self.mock_provider.sent_emails[-1]
            self.assertEqual(last['to'], 'candidate@example.com')
            self.assertEqual(last['from'], 'support.zarvanai@gmail.com')
            self.assertIn('Welcome to Zavran AI', last['subject'])
            self.assertIn('Alex Mercer', last['text'])
            self.assertIn('Zavran AI', last['html'])
            self.assertIn('data:image/png;base64,', last['html'])
        asyncio.run(run())

    def test_2_interview_scheduled_email_generation_and_dispatch(self):
        async def run():
            res = await EmailService.send_interview_scheduled_email(
                to_email='candidate@example.com',
                candidate_name='Alex Mercer',
                room_code='ZAV-99123',
                role='Staff AI Infrastructure Architect',
                company='HyperScale Labs',
                interviewer_name='Zaroon',
                interview_date='Today',
                interview_time='2:00 PM - 2:30 PM',
            )
            self.assertTrue(res.get('success'))
            last = self.mock_provider.sent_emails[-1]
            self.assertEqual(last['to'], 'candidate@example.com')
            self.assertEqual(last['from'], 'support.zarvanai@gmail.com')
            self.assertIn('Staff AI Infrastructure Architect', last['subject'])
            self.assertIn('ZAV-99123', last['text'])
            self.assertIn('HyperScale Labs', last['text'])
            self.assertIn('data:image/png;base64,', last['html'])
        asyncio.run(run())

    def test_3_interview_room_ready_email_dispatch(self):
        async def run():
            res = await EmailService.send_interview_ready_email(
                to_email='candidate@example.com',
                candidate_name='Alex Mercer',
                room_code='ZAV-99123',
                company='HyperScale Labs',
                role='Staff AI Infrastructure Architect',
                organization='HyperScale Labs',
                interviewer_name='Zaroon',
                interview_date='Today',
                interview_time='2:00 PM - 2:30 PM',
            )
            self.assertTrue(res.get('success'))
            last = self.mock_provider.sent_emails[-1]
            self.assertIn('Your Interview Room is Ready', last['subject'])
            self.assertIn('interview-room.html', last['text'])
            self.assertIn('ZAV-99123', last['html'])
        asyncio.run(run())

    def test_4_interview_completed_email_dispatch(self):
        async def run():
            res = await EmailService.send_interview_completed_email(
                to_email='candidate@example.com',
                candidate_name='Alex Mercer',
                room_code='ZAV-99123',
                role='Staff AI Infrastructure Architect',
                organization='HyperScale Labs',
                duration_str='28 minutes',
            )
            self.assertTrue(res.get('success'))
            last = self.mock_provider.sent_emails[-1]
            self.assertIn('Interview Completed', last['subject'])
            self.assertIn('10 minutes', last['text'])
            self.assertIn('28 minutes', last['text'])
        asyncio.run(run())

    def test_5_report_feedback_email_dispatch_with_10min_review(self):
        async def run():
            dummy_report = {
                'candidate': 'Alex Mercer',
                'role': 'Staff AI Infrastructure Architect',
                'overall_score': 92,
                'status': 'Strong Fit - Recommended for Staff Level',
                'summary': 'Exceptional architectural reasoning on low-latency streaming.',
                'interviewer': 'Zaroon AI',
            }
            res = await EmailService.send_candidate_report_email(
                to_email='candidate@example.com',
                candidate_name='Alex Mercer',
                report_id='ZAV-99123',
                report=dummy_report,
            )
            self.assertTrue(res.get('success'))
            last = self.mock_provider.sent_emails[-1]
            self.assertIn('Interview Feedback Report', last['subject'])
            self.assertIn('92/100', last['subject'])
            self.assertIn('Strong Fit', last['text'])
            self.assertIn('92', last['html'])
        asyncio.run(run())

    def test_rest_endpoints_welcome_and_schedule(self):
        resp1 = self.client.post('/api/auth/welcome-email', json={
            'candidate_name': 'Jane Doe',
            'email': 'jane@example.com'
        })
        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(resp1.json().get('success'))

        resp2 = self.client.post('/api/interview/schedule-email', json={
            'candidate_name': 'Jane Doe',
            'email': 'jane@example.com',
            'room_code': 'ZAV-TEST-441',
            'role': 'Backend AI Engineer',
            'company': 'Google',
            'organization': 'Google',
            'interviewer_name': 'Zaroon',
            'interview_date': 'Today',
            'interview_time': '4:00 PM - 4:30 PM'
        })
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.json().get('success'))

        resp3 = self.client.post('/api/interview/ZAV-TEST-441/ready-email', json={
            'company': 'Google',
            'role': 'Backend AI Engineer',
            'email': 'jane@example.com'
        })
        self.assertEqual(resp3.status_code, 200)
        self.assertTrue(resp3.json().get('success'))

        resp4 = self.client.post('/api/interview/ZAV-TEST-441/completed-email')
        self.assertEqual(resp4.status_code, 200)
        self.assertTrue(resp4.json().get('success'))

if __name__ == '__main__':
    unittest.main()
