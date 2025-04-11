from flask import Blueprint, jsonify, request, session, render_template
from datetime import datetime
from typing import Dict, List, Optional
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from db.utils import save_card
from db import SessionLocal
import re
import logging
import uuid
from core import DROECore
from utils.logger import get_logger

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interview_bp = Blueprint('interview', __name__)
core = DROECore()

INTERVIEW_QUESTIONS = {
    "welcome": [
        {"question": "Are you ready to begin your life story interview?", "type": "text"}
    ],
    "foundations": [
        {"question": "What is your full name and when were you born?", "type": "text"},
        {"question": "Where were you born and where did you grow up?", "type": "text"},
        {"question": "Tell me about your parents and siblings.", "type": "text"},
        {"question": "What are your earliest memories?", "type": "text"}
    ],
    "childhood": [
        {"question": "What was your childhood home like?", "type": "text"},
        {"question": "What were your favorite activities as a child?", "type": "text"},
        {"question": "Who were your closest friends growing up?", "type": "text"}
    ],
    "education": [
        {"question": "What schools did you attend and what were your experiences there?", "type": "text"},
        {"question": "What were your favorite subjects or activities in school?", "type": "text"}
    ]
}

class InterviewStage:
    def __init__(self):
        self.current_stage = "welcome"
        self.current_question_index = 0
        self.answers = []
        self.completed = False
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "current_stage": self.current_stage,
            "current_question_index": self.current_question_index,
            "answers": self.answers,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'InterviewStage':
        if not isinstance(data, dict):
            raise ValueError("Invalid data format for InterviewStage")

        instance = cls()
        instance.current_stage = data.get("current_stage", "welcome")
        instance.current_question_index = data.get("current_question_index", 0)
        instance.answers = data.get("answers", [])
        instance.completed = data.get("completed", False)
        instance.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        return instance

    def advance(self) -> bool:
        """Advance to next question or stage, returns True if interview is complete"""
        if self.completed:
            return True

        current_stage_questions = INTERVIEW_QUESTIONS.get(self.current_stage, [])

        if self.current_question_index < len(current_stage_questions) - 1:
            self.current_question_index += 1
            return False

        stages = list(INTERVIEW_QUESTIONS.keys())
        try:
            current_stage_index = stages.index(self.current_stage)
        except ValueError:
            self.completed = True
            return True

        if current_stage_index < len(stages) - 1:
            self.current_stage = stages[current_stage_index + 1]
            self.current_question_index = 0
            return False

        self.completed = True
        return True

    def get_current_question(self) -> Optional[Dict]:
        if self.completed:
            return None

        current_stage_questions = INTERVIEW_QUESTIONS.get(self.current_stage, [])
        if self.current_question_index < len(current_stage_questions):
            return current_stage_questions[self.current_question_index]
        return None

    def get_progress(self) -> float:
        if self.completed:
            return 100.0

        total_questions = sum(len(questions) for questions in INTERVIEW_QUESTIONS.values())
        if total_questions == 0:
            return 0.0

        completed_questions = 0
        stages = list(INTERVIEW_QUESTIONS.keys())

        try:
            current_stage_index = stages.index(self.current_stage)
        except ValueError:
            return 0.0

        # Add completed stages
        for stage in stages[:current_stage_index]:
            completed_questions += len(INTERVIEW_QUESTIONS[stage])

        # Add current stage progress
        completed_questions += self.current_question_index

        return (completed_questions / total_questions) * 100

@interview_bp.route('/interview', methods=['GET'], strict_slashes=False)
def get_interview():
    """Get the interview page."""
    try:
        if 'interview_stage' not in session:
            session['interview_stage'] = InterviewStage().to_dict()

        stage = InterviewStage.from_dict(session['interview_stage'])

        # Reset to welcome stage if current stage is invalid
        if stage.current_stage not in INTERVIEW_QUESTIONS:
            stage = InterviewStage()
            session['interview_stage'] = stage.to_dict()

        if stage.completed:
            response = {
                "question": "Thank you for sharing your story!",
                "completed": True,
                "current_stage": stage.current_stage,
                "progress": 100
            }
            return jsonify(response)

        question_data = stage.get_current_question()
        if not question_data:
            return jsonify({"error": "No question available"}), 400

        session['interview_stage'] = stage.to_dict()
        response = {
            "question": question_data["question"],
            "current_stage": stage.current_stage,
            "progress": stage.get_progress()
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@interview_bp.route('/interview', methods=['POST'], strict_slashes=False)
def process_interview():
    """Process interview responses and create cards."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'answer' not in data:
            return jsonify({"error": "No answer provided"}), 400
        
        if 'interview_stage' not in session:
            return jsonify({"error": "No active interview session"}), 400
        
        stage = InterviewStage.from_dict(session['interview_stage'])
        if stage.completed:
            return jsonify({"error": "Interview already completed"}), 400
        
        # Store the answer
        stage.answers.append({
            "question": stage.get_current_question()["question"],
            "answer": data["answer"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Advance to next question
        has_next = stage.advance()
        
        # Update session
        session['interview_stage'] = stage.to_dict()
        
        response = {
            "success": True,
            "has_next": has_next
        }
        
        if has_next:
            response["next_question"] = stage.get_current_question()
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error processing interview: {str(e)}")
        return jsonify({"error": str(e)}), 500

@interview_bp.route('/interview/process', methods=['POST'], strict_slashes=False)
def process_response():
    """Process a response and create appropriate cards."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data or 'response' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        
        response_data = data['response']
        core = DROECore()
        
        # Process different types of responses
        if 'people' in response_data:
            for person in response_data['people']:
                core.create_person(
                    name=person['name'],
                    title=person['title'],
                    description=person['description']
                )
        
        if 'location' in response_data:
            loc = response_data['location']
            core.create_place(
                name=loc['name'],
                title=loc['title'],
                description=loc['description'],
                latitude=loc.get('latitude'),
                longitude=loc.get('longitude')
            )
        
        if 'memory' in response_data:
            mem = response_data['memory']
            core.create_memory(
                title=mem['title'],
                description=mem['description']
            )
        
        return jsonify({"success": True})
    
    except Exception as e:
        logger.error(f"Error processing interview: {str(e)}")
        return jsonify({"error": str(e)}), 500