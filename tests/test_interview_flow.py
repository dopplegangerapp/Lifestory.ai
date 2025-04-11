import unittest
import json
from flask import Flask
from routes.interview import interview_bp, InterviewStage, INTERVIEW_QUESTIONS
from db.session_db import session_db
import os
import uuid
from datetime import datetime
import sqlite3
import time

class TestInterviewFlow(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.register_blueprint(interview_bp)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Set up test database path
        self.db_path = "test_sessions.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                time.sleep(1)  # Wait for any existing connections to close
                os.remove(self.db_path)
        
        # Close any existing connection and reinitialize with test database
        session_db.close()
        session_db.db_path = self.db_path
        session_db._init_db()
        self.db = session_db

    def test_complete_interview_flow(self):
        """Test the complete interview flow from start to finish"""
        # Start the interview
        response = self.client.get('/interview')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question'], "Where were you born and where did you grow up?")
        
        # Get session ID from cookie
        session_id = response.headers.get('Set-Cookie', '').split('session_id=')[1].split(';')[0]
        self.assertIsNotNone(session_id)
        
        # Answer first question
        response = self.client.post('/interview', 
            json={'answer': 'Portland, OR'},
            headers={'Cookie': f'session_id={session_id}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['next_question'], "Tell me about your parents and siblings.")
        
        # Answer second question
        response = self.client.post('/interview', 
            json={'answer': 'My Mom was an addict, my Dad wasnt around and my brother was in jail'},
            headers={'Cookie': f'session_id={session_id}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['next_question'], "What are your earliest memories?")
        
        # Answer third question
        response = self.client.post('/interview', 
            json={'answer': 'My earliest memory is playing in the park with my brother'},
            headers={'Cookie': f'session_id={session_id}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_stage'], 'childhood')
        self.assertEqual(data['next_question'], "What was your childhood home like?")
        
        # Verify session data
        session_data = self.db.get_session(session_id)
        self.assertIsNotNone(session_data)
        stage = InterviewStage.from_dict(session_data['interview_stage'])
        self.assertEqual(stage.current_stage, 'childhood')
        self.assertEqual(stage.current_question_index, 0)
        self.assertEqual(len(stage.answers), 3)

    def test_session_persistence(self):
        """Test that session data persists between requests"""
        # Start interview
        response = self.client.get('/interview')
        session_id = response.headers.get('Set-Cookie', '').split('session_id=')[1].split(';')[0]
        
        # Answer first question
        self.client.post('/interview', 
            json={'answer': 'Portland, OR'},
            headers={'Cookie': f'session_id={session_id}'}
        )
        
        # Get current state
        response = self.client.get('/interview', 
            headers={'Cookie': f'session_id={session_id}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['question'], "Tell me about your parents and siblings.")
        
        # Verify session data
        session_data = self.db.get_session(session_id)
        stage = InterviewStage.from_dict(session_data['interview_stage'])
        self.assertEqual(stage.current_question_index, 1)
        self.assertEqual(len(stage.answers), 1)

    def test_invalid_session(self):
        """Test behavior with invalid session"""
        # Try to continue interview with invalid session
        response = self.client.post('/interview', 
            json={'answer': 'Test answer'},
            headers={'Cookie': 'session_id=invalid_session_id'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question'], "Where were you born and where did you grow up?")

    def test_empty_answer(self):
        """Test handling of empty answers"""
        # Start interview
        response = self.client.get('/interview')
        session_id = response.headers.get('Set-Cookie', '').split('session_id=')[1].split(';')[0]
        
        # Submit empty answer
        response = self.client.post('/interview', 
            json={'answer': ''},
            headers={'Cookie': f'session_id={session_id}'}
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], "Answer cannot be empty")

    def tearDown(self):
        # Close the database connection
        if hasattr(self, 'db'):
            self.db.close()
            
        # Clean up test database
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                # If file is locked, try to close any open connections
                import gc
                gc.collect()
                time.sleep(1)  # Wait for any existing connections to close
                try:
                    os.remove(self.db_path)
                except PermissionError:
                    pass  # If still can't delete, let it be handled in next test's setUp

if __name__ == '__main__':
    unittest.main() 