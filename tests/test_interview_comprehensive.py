import pytest
import requests
import json
import time
from datetime import datetime
import sys
import os
import threading
import signal
from typing import Dict, List, Optional

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.interview import InterviewStage, interview_bp, INTERVIEW_QUESTIONS
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from db.utils import get_all_cards
from db import SessionLocal, init_db, engine, Base
from api import app

class TestInterviewComprehensive:
    @classmethod
    def setup_class(cls):
        """Setup test environment once for all tests"""
        # Initialize database
        Base.metadata.drop_all(engine)  # Clear existing tables
        Base.metadata.create_all(engine)  # Create new tables
        
        # Start Flask server in a separate thread
        def run_flask():
            app.run(host='localhost', port=5001)
            
        cls.flask_thread = threading.Thread(target=run_flask)
        cls.flask_thread.daemon = True
        cls.flask_thread.start()
        
        # Wait for server to start
        time.sleep(1)

    def setup_method(self):
        """Setup test environment for each test"""
        self.base_url = "http://localhost:5001"  # API server port
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.generated_cards = {
            "EventCard": False,
            "MemoryCard": False,
            "PersonCard": False,
            "PlaceCard": False
        }

    def teardown_method(self):
        """Cleanup test environment after each test"""
        self.session.close()

    @classmethod
    def teardown_class(cls):
        """Cleanup test environment after all tests"""
        # Stop Flask server
        os.kill(os.getpid(), signal.SIGINT)
        cls.flask_thread.join(timeout=1)
        
        # Clear database
        Base.metadata.drop_all(engine)

    def get_question(self) -> Dict:
        """Get current question"""
        response = self.session.get(f"{self.base_url}/interview")
        assert response.status_code == 200, f"Failed to get question: {response.text}"
        data = response.json()
        assert "question" in data, "Response missing question field"
        return data

    def submit_answer(self, answer: str) -> Dict:
        """Submit answer to current question"""
        response = self.session.post(
            f"{self.base_url}/interview",
            headers=self.headers,
            json={"answer": answer}
        )
        assert response.status_code == 200, f"Failed to submit answer: {response.text}"
        data = response.json()
        return data

    def test_complete_interview_with_cards(self):
        """Test complete interview flow with card generation"""
        # Start interview
        question = self.get_question()
        assert "question" in question, "Response missing question field"

        # Submit ready answer
        response = self.submit_answer("Yes, I'm ready")
        assert "next_question" in response, "Response missing next_question field"

        # Continue with questions that should generate cards
        max_questions = 20  # Prevent infinite loop
        question_count = 0
        
        while question_count < max_questions:
            question = self.get_question()
            question_text = question["question"].lower()
            
            # Default answer if no condition matches
            answer = "I prefer not to answer this question"
            
            # Match question type and provide appropriate answer
            if "name" in question_text or "born" in question_text:
                answer = "My name is John Smith, born on January 1, 1990 in New York City"
            elif "parent" in question_text or "famil" in question_text:
                answer = "My parents are Mary and John Smith. I have two siblings, Jane and Bob"
            elif "memor" in question_text:
                answer = "My earliest memory is playing in the park with my family"
            elif "home" in question_text or "live" in question_text:
                answer = "I grew up in a small house with a big backyard in Brooklyn"
            elif "activit" in question_text or "hobby" in question_text:
                answer = "I loved playing soccer and reading books"
            elif "friend" in question_text:
                answer = "My best friends were Tom and Sarah"
            elif "school" in question_text:
                answer = "I went to Brooklyn Elementary School"
            elif "job" in question_text or "work" in question_text:
                answer = "I worked as a software engineer at Tech Corp"
            elif "achievement" in question_text:
                answer = "I won the state chess championship"
            
            response = self.submit_answer(answer)
            
            # Check if any cards were created
            if "card_created" in response:
                card_type = response["card_created"]
                self.generated_cards[card_type] = True
            
            # Check if interview is complete
            if response.get("completed", False):
                break
                
            question_count += 1

        # Verify at least some cards were generated
        generated_count = sum(1 for v in self.generated_cards.values() if v)
        assert generated_count > 0, f"No cards were generated during the interview: {self.generated_cards}"

        # Verify cards in database
        db = SessionLocal()
        try:
            cards = get_all_cards(db)
            assert len(cards) > 0, "No cards found in database"
            card_types = {type(card).__name__ for card in cards}
            assert len(card_types) > 0, f"No card types found in database"
        finally:
            db.close()

    def test_error_handling(self):
        """Test error handling"""
        # Test empty answer
        response = self.session.post(
            f"{self.base_url}/interview",
            headers=self.headers,
            json={"answer": ""}
        )
        assert response.status_code == 400, "Expected 400 for empty answer"

        # Test invalid JSON
        response = self.session.post(
            f"{self.base_url}/interview",
            headers=self.headers,
            data="invalid json"
        )
        assert response.status_code == 400, "Expected 400 for invalid JSON"

        # Test missing answer field
        response = self.session.post(
            f"{self.base_url}/interview",
            headers=self.headers,
            json={}
        )
        assert response.status_code == 400, "Expected 400 for missing answer field"

    def test_interview_responses(self):
        """Test interview response formats"""
        # Get initial question
        response = self.get_question()
        assert "question" in response, "Response missing question field"
        assert isinstance(response["question"], str), "Question should be a string"

        # Submit answer and verify response format
        response = self.submit_answer("Yes")
        assert "next_question" in response, "Response missing next_question field"
        assert isinstance(response["next_question"], str), "next_question should be a string" 