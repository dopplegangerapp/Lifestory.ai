import pytest
import requests
import json
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.interview import InterviewStage, interview_bp, INTERVIEW_QUESTIONS
from flask import Flask, session
from core import DROECore
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from .test_base import TestBase

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(interview_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test interview stage initialization
def test_interview_stage_initialization():
    stage = InterviewStage()
    assert stage.current_stage == "welcome"
    assert stage.current_question_index == 0
    assert stage.answers == []
    assert stage.completed == False

# Test interview stage to dict
def test_interview_stage_to_dict():
    stage = InterviewStage()
    stage_dict = stage.to_dict()
    assert isinstance(stage_dict, dict)
    assert "current_stage" in stage_dict
    assert "current_question_index" in stage_dict
    assert "answers" in stage_dict
    assert "completed" in stage_dict
    assert "created_at" in stage_dict

# Test interview stage from dict
def test_interview_stage_from_dict():
    stage = InterviewStage()
    stage_dict = stage.to_dict()
    new_stage = InterviewStage.from_dict(stage_dict)
    assert new_stage.current_stage == stage.current_stage
    assert new_stage.current_question_index == stage.current_question_index
    assert new_stage.completed == stage.completed

# Test interview stage advancement
def test_interview_stage_advancement():
    stage = InterviewStage()
    # Test welcome stage
    assert stage.get_current_question()["question"] == "Are you ready to begin your life story interview?"
    stage.advance()
    # Test foundations stage
    assert stage.current_stage == "foundations"
    assert stage.get_current_question()["question"] == "What is your full name and when were you born?"

# Test progress calculation
def test_progress_calculation():
    stage = InterviewStage()
    # Initial progress
    initial_progress = stage.get_progress()
    assert initial_progress >= 0.0
    assert initial_progress <= 100.0
    
    # Progress after advancing
    stage.advance()
    new_progress = stage.get_progress()
    assert new_progress > initial_progress
    assert new_progress <= 100.0

# Test API endpoints
def test_get_initial_question(client):
    response = client.get('/interview')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "question" in data
    assert data["current_stage"] == "welcome"
    assert "progress" in data

def test_submit_valid_answer(client):
    # First get initial question
    client.get('/interview')
    
    # Submit answer
    response = client.post('/interview',
                         json={"answer": "Yes, I am ready"},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "success" in data
    assert data["success"] == True
    assert "next_question" in data

def test_submit_empty_answer(client):
    # First get initial question
    client.get('/interview')
    
    # Submit empty answer
    response = client.post('/interview',
                         json={"answer": ""},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_submit_missing_answer(client):
    # First get initial question
    client.get('/interview')
    
    # Submit without answer field
    response = client.post('/interview',
                         json={},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Test session management
def test_session_persistence(client):
    # Start interview
    response = client.get('/interview')
    assert response.status_code == 200
    initial_data = json.loads(response.data)
    
    # Submit answer
    response = client.post('/interview',
                         json={"answer": "Test answer"},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    
    # Get next question
    response = client.get('/interview')
    assert response.status_code == 200
    new_data = json.loads(response.data)
    
    # Verify progression
    assert new_data["current_stage"] != initial_data["current_stage"] or \
           new_data["question"] != initial_data["question"]

# Test interview completion
def test_complete_interview(client):
    # Get through all questions
    total_questions = sum(len(questions) for questions in INTERVIEW_QUESTIONS.values())
    answered = 0
    
    while answered < total_questions:
        # Get current question
        response = client.get('/interview')
        assert response.status_code == 200
        
        # Submit answer
        response = client.post('/interview',
                             json={"answer": f"Test answer {answered}"},
                             headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
        answered += 1
        
        data = json.loads(response.data)
        if not data.get("has_next", True):
            break
    
    # Verify completion
    response = client.get('/interview')
    data = json.loads(response.data)
    assert "completed" in data
    assert data["completed"] == True

# Test frontend integration
def test_frontend_integration():
    try:
        # Create a session
        session = requests.Session()

        # Test API endpoint availability
        response = session.get('http://localhost:5001/interview')
        assert response.status_code == 200

        # Test API response format
        data = response.json()
        assert "question" in data
        assert "current_stage" in data
        assert "progress" in data

        # Test answer submission
        headers = {'Content-Type': 'application/json'}
        response = session.post(
            'http://localhost:5001/interview',
            json={"answer": "Test answer"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] == True

    except requests.exceptions.ConnectionError:
        pytest.skip("Flask server is not running on port 5001. Start the server with 'python app.py' before running this test.")

# Test malformed JSON data
def test_malformed_json(client):
    # First get initial question
    client.get('/interview')
    
    # Submit malformed JSON
    response = client.post('/interview',
                         data="not a json",
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Test session corruption
def test_session_corruption(client):
    # Start interview
    response = client.get('/interview')
    assert response.status_code == 200
    
    # Corrupt session data
    with client.session_transaction() as sess:
        sess['interview_stage'] = "invalid data"
    
    # Try to get next question
    response = client.get('/interview')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data

# Test concurrent access simulation
def test_concurrent_access(client):
    # Start interview
    response = client.get('/interview')
    assert response.status_code == 200
    
    # Simulate concurrent access by modifying session directly
    with client.session_transaction() as sess:
        sess['interview_stage'] = InterviewStage().to_dict()
    
    # Try to get next question
    response = client.get('/interview')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "question" in data

# Test invalid stage transition
def test_invalid_stage_transition(client):
    # Start interview
    response = client.get('/interview')
    assert response.status_code == 200
    
    # Force invalid stage
    with client.session_transaction() as sess:
        stage = InterviewStage.from_dict(sess['interview_stage'])
        stage.current_stage = "invalid_stage"
        sess['interview_stage'] = stage.to_dict()
    
    # Try to get next question
    response = client.get('/interview')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["current_stage"] == "welcome"  # Should reset to welcome

# Test answer length limits
def test_answer_length_limits(client):
    # First get initial question
    client.get('/interview')
    
    # Submit very long answer
    long_answer = "a" * 10000  # 10k characters
    response = client.post('/interview',
                         json={"answer": long_answer},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

# Test special characters
def test_special_characters(client):
    # First get initial question
    client.get('/interview')
    
    # Submit answer with special characters
    special_answer = "Test answer with special chars: !@#$%^&*()_+{}|:\"<>?[]\\;',./`~"
    response = client.post('/interview',
                         json={"answer": special_answer},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

# Test trailing slash handling
def test_trailing_slash_handling(client):
    # Test GET with trailing slash
    response = client.get('/interview/')
    assert response.status_code == 200
    
    # Test POST with trailing slash
    response = client.post('/interview/',
                         json={"answer": "Test answer"},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

# Test malformed headers
def test_malformed_headers(client):
    # Test without Content-Type header
    response = client.post('/interview',
                         data=json.dumps({"answer": "Test answer"}))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Test request body format
def test_request_body_format(client):
    # Test with non-JSON body
    response = client.post('/interview',
                         data="not json",
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Test redirect handling
def test_redirect_handling(client):
    # Test POST to /interview (should work without redirect)
    response = client.post('/interview',
                         json={"answer": "Test answer"},
                         headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "success" in data

# Test concurrent requests
def test_concurrent_requests(client):
    # Start interview
    response = client.get('/interview')
    assert response.status_code == 200
    
    # Simulate concurrent POST requests
    response1 = client.post('/interview',
                         json={"answer": "First answer"},
                         headers={'Content-Type': 'application/json'})
    response2 = client.post('/interview',
                         json={"answer": "Second answer"},
                         headers={'Content-Type': 'application/json'})
    
    assert response1.status_code == 200
    assert response2.status_code == 200

class TestInterview(TestBase):
    def setUp(self):
        super().setUp()
        self.app.register_blueprint(interview_bp)
        
    def test_submit_answer_person(self):
        with self.app.test_client() as client:
            # Submit person answer
            response = client.post('/interview/process',
                                json={
                                    "response": {
                                        "people": [{
                                            "name": "John Doe",
                                            "title": "John Doe",
                                            "description": "A test person"
                                        }]
                                    }
                                },
                                headers={'Content-Type': 'application/json'})
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] == True
            
    def test_submit_answer_place(self):
        with self.app.test_client() as client:
            # Submit place answer
            response = client.post('/interview/process',
                                json={
                                    "response": {
                                        "location": {
                                            "name": "New York City",
                                            "title": "New York City",
                                            "description": "A test place",
                                            "latitude": 40.7128,
                                            "longitude": -74.0060
                                        }
                                    }
                                },
                                headers={'Content-Type': 'application/json'})
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] == True
            
    def test_submit_answer_memory(self):
        with self.app.test_client() as client:
            # Submit memory answer
            response = client.post('/interview/process',
                                json={
                                    "response": {
                                        "memory": {
                                            "title": "First day at school",
                                            "description": "A test memory"
                                        }
                                    }
                                },
                                headers={'Content-Type': 'application/json'})
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] == True

if __name__ == '__main__':
    pytest.main([__file__])
