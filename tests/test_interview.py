
import unittest
from flask import Flask, session
from routes.interview import interview_bp, InterviewStage
import json

class TestInterview(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.register_blueprint(interview_bp, url_prefix='/interview')
        self.client = self.app.test_client()

    def test_get_initial_question(self):
        with self.app.test_client() as client:
            response = client.get('/interview/')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('question', data)
            self.assertIn('current_stage', data)
            self.assertIn('progress', data)

    def test_submit_valid_answer(self):
        with self.app.test_client() as client:
            # Start interview
            client.get('/interview/')
            
            # Submit answer
            response = client.post('/interview/', 
                                 json={'answer': 'Test answer'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('next_question', data)

    def test_submit_empty_answer(self):
        with self.app.test_client() as client:
            client.get('/interview/')
            response = client.post('/interview/', 
                                 json={'answer': ''})
            self.assertEqual(response.status_code, 400)

    def test_interview_completion(self):
        with self.app.test_client() as client:
            client.get('/interview/')
            
            # Complete all questions
            for _ in range(len(InterviewStage.INTERVIEW_QUESTIONS)):
                response = client.post('/interview/', 
                                     json={'answer': 'Test answer'})
                if response.json.get('completed'):
                    break
                    
            self.assertTrue(response.json.get('completed'))

if __name__ == '__main__':
    unittest.main()
