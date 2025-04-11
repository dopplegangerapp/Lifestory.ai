
import unittest
from flask import Flask, session
from routes.interview import interview_bp, InterviewStage
import json

class TestInterview(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.register_blueprint(interview_bp)
        self.client = self.app.test_client()
        self.stage = InterviewStage()

    def test_interview_get_initial_question(self):
        """Test getting the initial interview question."""
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('question', data)
            self.assertEqual(data['current_stage'], 'welcome')
            self.assertGreaterEqual(float(data['progress']), 0)

    def test_interview_submit_answer(self):
        """Test submitting an answer and getting next question."""
        with self.app.test_client() as client:
            # First get initial question
            client.get('/')
            
            # Submit answer
            response = client.post('/', json={
                'answer': 'John Doe',
                'stage': 'welcome'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get('success'))
            self.assertIn('next_question', data)
            self.assertIn('current_stage', data)
            self.assertIn('progress', data)

    def test_interview_empty_answer(self):
        """Test submitting empty answer."""
        with self.app.test_client() as client:
            response = client.post('/', json={
                'answer': '',
                'stage': 'welcome'
            })
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)

    def test_interview_invalid_request(self):
        """Test invalid request format."""
        with self.app.test_client() as client:
            response = client.post('/', json={})
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
