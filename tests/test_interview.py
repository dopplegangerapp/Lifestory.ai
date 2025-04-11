
import unittest
from flask import Flask, session
from routes.interview import interview_bp, InterviewStage, INTERVIEW_QUESTIONS
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
            self.assertEqual(data['current_stage'], 'welcome')
            self.assertIn('progress', data)
            self.assertGreaterEqual(data['progress'], 0)

    def test_submit_valid_answer(self):
        with self.app.test_client() as client:
            # Start interview
            response = client.get('/interview/')
            self.assertEqual(response.status_code, 200)
            
            # Submit answer
            response = client.post('/interview/', 
                                 json={'answer': 'Test answer'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('next_question', data)
            self.assertFalse(data['completed'])

    def test_submit_empty_answer(self):
        with self.app.test_client() as client:
            client.get('/interview/')
            response = client.post('/interview/', 
                                 json={'answer': ''})
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Answer cannot be empty')

    def test_interview_completion(self):
        with self.app.test_client() as client:
            # Get initial question
            response = client.get('/interview/')
            self.assertEqual(response.status_code, 200)
            
            # Complete all questions
            total_questions = sum(len(questions) for questions in INTERVIEW_QUESTIONS.values())
            
            for _ in range(total_questions):
                response = client.post('/interview/', 
                                     json={'answer': 'Test answer'})
                data = json.loads(response.data)
                
                if data.get('completed'):
                    break
                    
                self.assertEqual(response.status_code, 200)
                self.assertTrue(data['success'])
                
            self.assertTrue(data['completed'])

    def test_invalid_request(self):
        with self.app.test_client() as client:
            response = client.post('/interview/', 
                                 json={'invalid': 'data'})
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
