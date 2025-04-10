from tests.test_base import TestBase
from routes.interview import InterviewStage
from ai.assistant import Assistant
import json
import unittest
from flask import Flask
from routes.interview import interview_bp
import os

class TestInterview(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.register_blueprint(interview_bp)
        self.client = self.app.test_client()
        
        # Create test context
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        
        # Initialize interview stage
        self.stage = InterviewStage()
    
    def tearDown(self):
        """Clean up after each test."""
        self.ctx.pop()
    
    def test_app_exists(self):
        """Test that Flask app exists."""
        self.assertIsNotNone(self.app)
    
    def test_app_is_testing(self):
        """Test that app is in testing mode."""
        self.assertTrue(self.app.config['TESTING'])
    
    def test_interview_stage_initialization(self):
        """Test initial state of interview stage."""
        self.assertEqual(self.stage.current_stage, 0)
        self.assertEqual(len(self.stage.answers), 0)
        self.assertFalse(self.stage.is_complete)
        self.assertIsNotNone(self.stage.assistant)
    
    def test_interview_stage_transition(self):
        """Test stage transition."""
        initial_stage = self.stage.current_stage
        self.stage.transition_stage()
        self.assertEqual(self.stage.current_stage, initial_stage + 1)
    
    def test_interview_stage_completion(self):
        """Test marking stage as complete."""
        self.stage.mark_complete()
        self.assertTrue(self.stage.is_complete)
    
    def test_interview_stage_reset(self):
        """Test resetting stage to initial state."""
        self.stage.transition_stage()
        self.stage.add_answer("Test answer")
        self.stage.mark_complete()
        
        self.stage.reset()
        self.assertEqual(self.stage.current_stage, 0)
        self.assertEqual(len(self.stage.answers), 0)
        self.assertFalse(self.stage.is_complete)
    
    def test_interview_stage_progress(self):
        """Test adding answers and tracking progress."""
        initial_answers = len(self.stage.answers)
        self.stage.add_answer("Test answer")
        self.assertEqual(len(self.stage.answers), initial_answers + 1)
    
    def test_interview_route_get(self):
        """Test GET request to interview endpoint."""
        response = self.client.get('/interview')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('current_stage', data)
        self.assertIn('question', data)
        self.assertIn('is_complete', data)
    
    def test_interview_route_post(self):
        """Test POST request to interview endpoint."""
        response = self.client.post('/interview',
                                  json={'answer': 'Test answer'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('next_question', data)
        self.assertIn('stage_complete', data)
    
    def test_interview_route_invalid_post(self):
        """Test POST request without answer."""
        response = self.client.post('/interview', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_interview_stage_serialization(self):
        """Test serialization and deserialization of interview stage."""
        # Add some test data
        self.stage.add_answer("Test answer")
        self.stage.transition_to("childhood")
        
        # Convert to dict
        stage_dict = self.stage.to_dict()
        
        # Verify dict contents
        self.assertEqual(stage_dict['current_stage'], "childhood")
        self.assertEqual(len(stage_dict['answers']), 1)
        self.assertEqual(stage_dict['answers'][0]['answer'], "Test answer")
        self.assertEqual(stage_dict['answers'][0]['stage'], "foundations")
        self.assertFalse(stage_dict['is_complete'])
        
        # Create new instance from dict
        new_stage = InterviewStage.from_dict(stage_dict)
        
        # Verify new instance
        self.assertEqual(new_stage.current_stage, self.stage.current_stage)
        self.assertEqual(len(new_stage.answers), len(self.stage.answers))
        self.assertEqual(new_stage.answers[0]['answer'], self.stage.answers[0]['answer'])
        self.assertEqual(new_stage.answers[0]['stage'], self.stage.answers[0]['stage'])
        self.assertEqual(new_stage.is_complete, self.stage.is_complete)
        self.assertIsNotNone(new_stage.assistant)
    
    def test_assistant_initialization(self):
        """Test that assistant is properly initialized."""
        self.assertIsNotNone(self.stage.assistant)
    
    def test_assistant_methods(self):
        """Test assistant methods are accessible."""
        self.assertTrue(hasattr(self.stage.assistant, 'create_message'))
        self.assertTrue(hasattr(self.stage.assistant, 'create_run'))
        self.assertTrue(hasattr(self.stage.assistant, 'get_response'))
        self.assertTrue(hasattr(self.stage.assistant, 'analyze_text'))
        self.assertTrue(hasattr(self.stage.assistant, 'generate_follow_up'))

    def test_interview_stage_initialization(self):
        self.assertEqual(self.stage.current_stage, "foundations")
        self.assertIsNotNone(self.stage.stages)
        self.assertIn("foundations", self.stage.stages)
    
    def test_interview_stage_transition(self):
        # Test valid stage transition
        self.assertTrue(self.stage.transition_to("childhood"))
        self.assertEqual(self.stage.current_stage, "childhood")
        
        # Test invalid stage transition
        self.assertFalse(self.stage.transition_to("invalid_stage"))
        self.assertEqual(self.stage.current_stage, "childhood")
    
    def test_interview_stage_completion(self):
        # Mark stage as complete
        self.stage.mark_complete()
        self.assertTrue(self.stage.is_complete)
        
        # Try to complete again
        self.stage.mark_complete()
        self.assertTrue(self.stage.is_complete)
    
    def test_interview_stage_progress(self):
        # Test stage progress tracking
        self.assertEqual(self.stage.get_progress(), 0)
        
        # Add some answers
        self.stage.add_answer("Test answer 1")
        self.stage.add_answer("Test answer 2")
        
        self.assertEqual(len(self.stage.answers), 2)
        self.assertGreater(self.stage.get_progress(), 0)
    
    def test_interview_stage_reset(self):
        # Test stage reset
        self.stage.add_answer("Test answer")
        self.stage.mark_complete()
        
        self.stage.reset()
        self.assertEqual(len(self.stage.answers), 0)
        self.assertFalse(self.stage.is_complete)
        self.assertEqual(self.stage.current_stage, "foundations") 