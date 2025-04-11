import unittest
from flask import Flask
from routes.interview import interview_bp, InterviewStage

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
        self.assertEqual(self.stage.current_stage, "welcome")
        self.assertEqual(len(self.stage.answers), 0)
        self.assertFalse(self.stage.completed)

    def test_interview_route_get(self):
        """Test GET request to interview endpoint."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_interview_route_post(self):
        """Test POST request to interview endpoint."""
        response = self.client.post('/',
                                  json={'answer': 'Test answer', 'stage': 'welcome'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue('success' in data)

    def test_interview_route_invalid_post(self):
        """Test POST request without answer."""
        response = self.client.post('/', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)