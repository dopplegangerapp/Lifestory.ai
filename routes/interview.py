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

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

interview_bp = Blueprint('interview', __name__)
core = DROECore()

INTERVIEW_QUESTIONS = {
    "welcome": [
        {"question": "Are you ready to begin your life story interview?"}
    ],
    "foundations": [
        {"question": "What is your full name and when were you born?"},
        {"question": "Where were you born and where did you grow up?"},
        {"question": "Tell me about your parents and siblings."},
        {"question": "What are your earliest memories?"}
    ],
    "childhood": [
        {"question": "What was your childhood home like?"},
        {"question": "What were your favorite activities as a child?"},
        {"question": "Who were your closest friends growing up?"}
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

@interview_bp.route('/interview', methods=['GET'])
def get_interview():
    """Get the interview page."""
    return render_template('interview.html')

@interview_bp.route('/interview', methods=['POST'])
def process_interview():
    """Process interview responses and create cards."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        response = data.get('response')
        if not response:
            return jsonify({'error': 'No response provided'}), 400
        
        # Process the response and create appropriate cards
        cards = []
        
        # Create event card if event information is present
        if 'event' in response:
            event_data = response['event']
            event = core.create_event(
                title=event_data.get('title', ''),
                description=event_data.get('description', ''),
                location=event_data.get('location'),
                participants=event_data.get('participants', [])
            )
            cards.append(event)
        
        # Create person cards if people information is present
        if 'people' in response:
            for person_data in response['people']:
                person = core.create_person(
                    title=person_data.get('title', ''),
                    description=person_data.get('description', ''),
                    name=person_data.get('name', '')
                )
                cards.append(person)
        
        # Create place card if location information is present
        if 'location' in response:
            place_data = response['location']
            place = core.create_place(
                title=place_data.get('title', ''),
                description=place_data.get('description', ''),
                name=place_data.get('name', ''),
                latitude=place_data.get('latitude', 0.0),
                longitude=place_data.get('longitude', 0.0)
            )
            cards.append(place)
        
        # Create memory card if memory information is present
        if 'memory' in response:
            memory_data = response['memory']
            memory = core.create_memory(
                title=memory_data.get('title', ''),
                description=memory_data.get('description', '')
            )
            cards.append(memory)
        
        # Save all created cards
        for card in cards:
            try:
                core.save_card(card)
            except Exception as e:
                logger.error(f"Error saving card: {str(e)}")
                continue
        
        return jsonify({
            'message': 'Cards created successfully',
            'cards': [card.to_dict() for card in cards]
        })
        
    except Exception as e:
        logger.error(f"Error processing interview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@interview_bp.route('', methods=['GET'])
@interview_bp.route('/', methods=['GET'])
def get_question():
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

@interview_bp.route('', methods=['POST'])
@interview_bp.route('/', methods=['POST'])
def submit_answer():
    try:
        # Initialize session if needed
        if 'interview_stage' not in session:
            session['interview_stage'] = InterviewStage().to_dict()

        stage = InterviewStage.from_dict(session['interview_stage'])
        
        # Check Content-Type header
        content_type = request.headers.get('Content-Type', '')
        if not content_type or 'application/json' not in content_type.lower():
            logger.error(f"Invalid Content-Type: {content_type}")
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        # Ensure request has JSON data
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        try:
            data = request.get_json()
        except Exception as e:
            logger.error(f"Invalid JSON data: {str(e)}")
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Check if answer field exists and is not empty
        if not data or 'answer' not in data:
            logger.error("No answer provided")
            return jsonify({"error": "No answer provided"}), 400

        answer = str(data['answer']).strip()
        if not answer:
            logger.error("Empty answer provided")
            return jsonify({"error": "Answer cannot be empty"}), 400

        current_question = stage.get_current_question()
        if not current_question:
            logger.error("No current question")
            return jsonify({"error": "No current question"}), 400

        logger.debug(f"Current question: {current_question['question']}")
        logger.debug(f"Current stage: {stage.current_stage}")

        # Store the answer
        stage.answers.append({
            "question": current_question["question"],
            "answer": answer,
            "stage": stage.current_stage,
            "timestamp": datetime.now().isoformat()
        })

        # Generate appropriate card based on stage and content
        card_created = None
        
        try:
            if stage.current_stage == "foundations":
                if "full name" in current_question["question"].lower():
                    logger.debug("Creating PersonCard for name/birth info")
                    # Create PersonCard for name/birth info
                    person = core.create_person(
                        title=answer.split()[0],  # First name as title
                        description=answer,
                        name=answer.split()[0],  # First name
                        relationship="Self"
                    )
                    card_created = "PersonCard"
                    logger.debug(f"Created PersonCard: {person}")
                
                elif "born" in current_question["question"].lower():
                    logger.debug("Creating PlaceCard for birthplace")
                    # Create PlaceCard for birthplace/growing up location
                    place = core.create_place(
                        title=answer.split()[0],  # First word as title
                        description=answer,
                        name=answer.split()[0],  # First word as name
                        latitude=0.0,
                        longitude=0.0
                    )
                    card_created = "PlaceCard"
                    logger.debug(f"Created PlaceCard: {place}")
                
                elif "parents and siblings" in current_question["question"].lower():
                    logger.debug("Creating PersonCard for family members")
                    # Create PersonCard for family members
                    person = core.create_person(
                        title=answer.split()[0],  # First name as title
                        description=answer,
                        name=answer.split()[0],  # First name
                        relationship="Family"
                    )
                    card_created = "PersonCard"
                    logger.debug(f"Created PersonCard: {person}")
                
                elif "earliest memories" in current_question["question"].lower():
                    logger.debug("Creating MemoryCard for early memories")
                    # Create MemoryCard for early memories
                    memory = core.create_memory(
                        title="Early Memory",
                        description=answer,
                        emotions=["Nostalgic", "Happy"]
                    )
                    card_created = "MemoryCard"
                    logger.debug(f"Created MemoryCard: {memory}")
            
            elif stage.current_stage == "childhood":
                if "childhood home" in current_question["question"].lower():
                    logger.debug("Creating PlaceCard for childhood home")
                    # Create PlaceCard for childhood home
                    place = core.create_place(
                        title="Childhood Home",
                        description=answer,
                        name="Childhood Home",
                        latitude=0.0,
                        longitude=0.0
                    )
                    card_created = "PlaceCard"
                    logger.debug(f"Created PlaceCard: {place}")
                
                elif "favorite activities" in current_question["question"].lower():
                    logger.debug("Creating EventCard for childhood activities")
                    # Create EventCard for childhood activities
                    event = core.create_event(
                        title="Childhood Activity",
                        description=answer,
                        start_date=datetime.now(),
                        end_date=None,
                        emotions=["Happy", "Nostalgic"]
                    )
                    card_created = "EventCard"
                    logger.debug(f"Created EventCard: {event}")
                
                elif "closest friends" in current_question["question"].lower():
                    logger.debug("Creating PersonCard for childhood friends")
                    # Create PersonCard for childhood friends
                    person = core.create_person(
                        title=answer.split()[0],  # First name as title
                        description=answer,
                        name=answer.split()[0],  # First name
                        relationship="Childhood Friend"
                    )
                    card_created = "PersonCard"
                    logger.debug(f"Created PersonCard: {person}")
            
        except Exception as e:
            logger.error(f"Error creating card: {str(e)}")
            print(f"Error creating card: {str(e)}")

        # Advance to next question
        is_complete = stage.advance()
        session['interview_stage'] = stage.to_dict()

        if is_complete:
            return jsonify({
                "completed": True,
                "success": True,
                "message": "Interview completed successfully",
                "card_created": card_created
            })

        next_question = stage.get_current_question()
        if not next_question:
            return jsonify({"error": "Failed to get next question"}), 500

        return jsonify({
            "success": True,
            "next_question": next_question["question"],
            "current_stage": stage.current_stage,
            "progress": stage.get_progress(),
            "completed": False,
            "card_created": card_created
        })
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500