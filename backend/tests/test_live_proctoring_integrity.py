import unittest
import time
from fastapi.testclient import TestClient
from backend.main import app
from backend.interview_engine import interview_engine
from backend.config import settings
from backend.providers.email_provider import EmailService, MockConsoleEmailProvider

class TestLiveProctoringIntegrity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_provider = MockConsoleEmailProvider()
        EmailService.set_provider(self.mock_provider)
        interview_engine.sessions.clear()
        interview_engine.user_interviews.clear()
        interview_engine.user_profiles.clear()
        interview_engine.user_dossiers.clear()

        self.user_id = 'usr_proctor_candidate_1'
        self.headers = {'Authorization': f'Bearer {self.user_id}'}
        self.room_code = 'ZAV-PROCTOR-999'

        # Schedule interview
        self.client.post('/api/user/interviews/schedule', headers=self.headers, json={
            'room_code': self.room_code,
            'role': 'Full Stack AI Engineer',
            'company': 'Zavran AI Partner',
            'candidate_name': 'Test Candidate'
        })

    def test_preinterview_validation_gating(self):
        # 1. Initially preinterview_validated is False
        sess_res = self.client.get(f'/api/interview/{self.room_code}/session', headers=self.headers).json()
        self.assertFalse(sess_res['session']['preinterview_validated'])

        # 2. Call /api/interview/{id}/validate-precheck
        val_res = self.client.post(
            f'/api/interview/{self.room_code}/validate-precheck',
            headers=self.headers,
            json={'checks_passed': True}
        )
        self.assertEqual(val_res.status_code, 200)
        self.assertTrue(val_res.json()['data']['preinterview_validated'])

        # 3. Verify session state reflects preinterview_validated
        sess_res2 = self.client.get(f'/api/interview/{self.room_code}/session', headers=self.headers).json()
        self.assertTrue(sess_res2['session']['preinterview_validated'])

    def test_violation_telemetry_and_authoritative_15_warning_termination(self):
        # Start the session
        self.client.post(f'/api/interview/{self.room_code}/start', headers=self.headers)

        session = interview_engine.sessions[self.room_code]
        self.assertEqual(session.status, 'in_progress')
        self.assertEqual(session.warning_count, 0)
        self.assertFalse(session.is_terminated)

        # Trigger violations 1 through 14 with structured telemetry
        violation_types = [
            'camera_off', 'face_missing', 'shoulders_missing', 'face_too_close',
            'insufficient_lighting', 'phone_detected', 'tab_switch', 'fullscreen_exit',
            'clipboard_copy', 'clipboard_paste', 'shortcut_violation', 'camera_covered',
            'mic_off', 'multiple_faces'
        ]

        for i, v_type in enumerate(violation_types, start=1):
            session.last_violation_incident_time = 0.0
            session.active_violations.clear()

            res = self.client.post(
                f'/api/interview/{self.room_code}/violation',
                headers=self.headers,
                json={
                    'event_type': v_type,
                    'details': f'Test violation {i}',
                    'confidence': 0.95,
                    'image_base64': 'data:image/jpeg;base64,mockevidenceframe',
                    'candidate_id': self.user_id,
                    'category': 'proctoring'
                }
            )
            self.assertEqual(res.status_code, 200)
            data = res.json()['result']
            self.assertEqual(data['action'], 'warn')
            self.assertEqual(data['warning_count'], i)
            self.assertEqual(data['max_warnings'], 15)
            self.assertEqual(session.warning_count, i)

        self.assertEqual(session.warning_count, 14)
        self.assertFalse(session.is_terminated)
        self.assertEqual(session.status, 'in_progress')

        # 15th Violation -> Authoritative Session Lock & Termination
        session.last_violation_incident_time = 0.0
        session.active_violations.clear()
        res_15 = self.client.post(
            f'/api/interview/{self.room_code}/violation',
            headers=self.headers,
            json={
                'event_type': 'tab_switch',
                'details': '15th violation trigger',
                'confidence': 1.0,
                'image_base64': None,
                'candidate_id': self.user_id
            }
        )
        self.assertEqual(res_15.status_code, 200)
        data_15 = res_15.json()['result']
        self.assertEqual(data_15['action'], 'terminate')
        self.assertEqual(data_15['warning_count'], 15)
        self.assertEqual(data_15['status'], 'unsuccessful')
        self.assertTrue(session.is_terminated)
        self.assertEqual(session.status, 'unsuccessful')
        self.assertEqual(session.completion_reason, 'max_warnings_exceeded')

        # Subsequent violation requests return immediate locked termination
        res_16 = self.client.post(
            f'/api/interview/{self.room_code}/violation',
            headers=self.headers,
            json={'event_type': 'face_missing'}
        )
        self.assertEqual(res_16.json()['result']['action'], 'terminate')
        self.assertEqual(res_16.json()['result']['warning_count'], 15)

        # Subsequent start attempt is rejected/returned as unsuccessful
        start_attempt = self.client.post(f'/api/interview/{self.room_code}/start', headers=self.headers).json()
        self.assertEqual(start_attempt['session']['status'], 'unsuccessful')
        self.assertTrue(start_attempt['session']['is_terminated'])

        # Subsequent process-response attempt is locked
        submit_attempt = self.client.post(
            f'/api/interview/{self.room_code}/process-response',
            headers=self.headers,
            json={'speech_text': 'I want to answer anyway'}
        ).json()
        self.assertTrue(submit_attempt['data']['is_finished'])
        self.assertEqual(submit_attempt['data']['session']['status'], 'unsuccessful')
        self.assertTrue(submit_attempt['data']['session']['is_terminated'])

        # Subsequent session query reflects permanently terminated safe state
        sess_state = self.client.get(f'/api/interview/{self.room_code}/session', headers=self.headers).json()['session']
        self.assertTrue(sess_state['is_terminated'])
        self.assertEqual(sess_state['status'], 'unsuccessful')
        self.assertEqual(sess_state['warning_count'], 15)
        self.assertEqual(sess_state['completion_reason'], 'max_warnings_exceeded')

    def test_violation_debounce_logic(self):
        self.client.post(f'/api/interview/{self.room_code}/start', headers=self.headers)
        session = interview_engine.sessions[self.room_code]

        # Trigger first violation
        res1 = self.client.post(
            f'/api/interview/{self.room_code}/violation',
            headers=self.headers,
            json={'event_type': 'face_missing', 'details': 'Face not visible'}
        ).json()['result']
        self.assertEqual(res1['action'], 'warn')
        self.assertEqual(res1['warning_count'], 1)

        # Immediately trigger same violation within debounce window (0.1s)
        res2 = self.client.post(
            f'/api/interview/{self.room_code}/violation',
            headers=self.headers,
            json={'event_type': 'face_missing', 'details': 'Face still not visible'}
        ).json()['result']
        self.assertEqual(res2['action'], 'debounced')
        self.assertEqual(res2['warning_count'], 1)
        self.assertEqual(session.warning_count, 1)

    def test_dynamic_recovery_recording(self):
        self.client.post(f'/api/interview/{self.room_code}/start', headers=self.headers)
        session = interview_engine.sessions[self.room_code]

        # Trigger violation
        self.client.post(
            f'/api/interview/{self.room_code}/violation',
            headers=self.headers,
            json={'event_type': 'face_missing', 'details': 'Face not visible'}
        )
        self.assertIn('face_missing', session.active_violations)

        # Record recovery
        rec_res = self.client.post(
            f'/api/interview/{self.room_code}/recovery',
            headers=self.headers,
            json={
                'recovered_type': 'face_missing',
                'details': 'Candidate face is now centered in the guide oval.'
            }
        )
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.json()['result']
        self.assertTrue(rec_data['success'])
        self.assertEqual(rec_data['recovered_type'], 'face_missing')
        self.assertNotIn('face_missing', session.active_violations)
        self.assertEqual(len(session.recoveries), 1)

if __name__ == '__main__':
    unittest.main()
