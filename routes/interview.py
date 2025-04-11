from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from datetime import datetime
from typing import Dict, List, Optional
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from cards.base_card import BaseCard
from db.utils import save_card
from db import SessionLocal
from db.session_db import session_db
import re
import logging
import uuid
from core import DROECore
from utils.logger import get_logger
from services.openai_service import OpenAIService
from models.interview_stage import InterviewStage
from services.event_card_service import create_event_card

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interview_bp = Blueprint('interview', __name__)
core = DROECore()
openai_service = OpenAIService()

@interview_bp.route('/interview', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_interview():
    """Get the current interview question."""
    try:
        # Get or create session ID
        session_id = request.cookies.get('session')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        # Get current stage
        current_stage = session.get('stage', 'start')
        
        # Get next question based on stage
        question = openai_service.get_next_question({
            'stage': current_stage,
            'context': session.get('context', {})
        })
        
        response = jsonify({
            'success': True,
            'question': question,
            'stage': current_stage,
            'session_id': session_id
        })
        
        # Set session cookie
        response.set_cookie('session', session_id)
        return response
        
    except Exception as e:
        logger.error(f"Error in get_interview: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

def extract_location(answer: str) -> str:
    """Extract location from answer text."""
    # Look for common location patterns
    location_patterns = [
        r'in ([^\.]+)',  # "in Portland, Oregon"
        r'from ([^\.]+)',  # "from New York City"
        r'at ([^\.]+)',  # "at 123 Main Street"
        r'to ([^\.]+)',  # "moved to Chicago"
        r'born in ([^\.]+)'  # "born in Los Angeles"
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, answer)
        if match:
            return match.group(1).strip()
    
    # If no pattern matches, return the first sentence
    return answer.split('.')[0].strip()

@interview_bp.route('/interview', methods=['POST'])
@cross_origin(supports_credentials=True)
def submit_answer():
    """Submit an answer to the current question."""
    try:
        # Get session ID from cookie
        session_id = request.cookies.get('session')
        if not session_id:
            return jsonify({
                'error': 'No session cookie found'
            }), 401
        
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        # Get answer from request
        data = request.get_json()
        if 'answer' not in data:
            return jsonify({
                'error': 'Missing answer in request body'
            }), 400
            
        answer = data['answer']
        
        # Get current stage
        current_stage = session.get('stage', 'start')
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Process answer based on stage
            if current_stage == 'start':
                # Extract location from answer
                location = extract_location(answer)
                
                # Create place card
                card = {
                    'id': str(uuid.uuid4()),
                    'type': 'place',
                    'title': f'Place: {location}',
                    'description': answer,
                    'date': datetime.now().isoformat(),
                    'image_url': None,
                    'session_id': session_id,
                    'location': location
                }
                
                # Generate image
                image_url = openai_service.generate_image(f"A place called {location}: {answer}")
                if image_url:
                    card['image_url'] = image_url
                
                # Save card to database
                save_card(db, card, session_id)
                
                # Update context
                session['context'] = {
                    'place': location,
                    'stage': 'family'
                }
                session['stage'] = 'family'
                
            elif current_stage == 'family':
                # Extract people from answer
                people = extract_people(answer)
                
                # Create person card
                card = {
                    'id': str(uuid.uuid4()),
                    'type': 'person',
                    'title': f'Family: {", ".join(people)}',
                    'description': answer,
                    'date': datetime.now().isoformat(),
                    'image_url': None,
                    'session_id': session_id,
                    'people': people
                }
                
                # Generate image
                image_url = openai_service.generate_image(f"A family portrait with {', '.join(people)}")
                if image_url:
                    card['image_url'] = image_url
                
                # Save card to database
                save_card(db, card, session_id)
                
                # Update context
                session['context'].update({
                    'family': people,
                    'stage': 'events'
                })
                session['stage'] = 'events'
                
            elif current_stage == 'events':
                # Extract date from answer
                date = extract_date(answer)
                
                # Create event card
                card = {
                    'id': str(uuid.uuid4()),
                    'type': 'event',
                    'title': 'Important Event',
                    'description': answer,
                    'date': date.isoformat() if date else datetime.now().isoformat(),
                    'image_url': None,
                    'session_id': session_id
                }
                
                # Generate image
                image_url = openai_service.generate_image(answer)
                if image_url:
                    card['image_url'] = image_url
                
                # Save card to database
                save_card(db, card, session_id)
                
                # Update context
                session['context'].update({
                    'events': answer,
                    'stage': 'memories'
                })
                session['stage'] = 'memories'
                
            else:  # memories stage
                # Create memory card
                card = {
                    'id': str(uuid.uuid4()),
                    'type': 'memory',
                    'title': 'Memory',
                    'description': answer,
                    'date': datetime.now().isoformat(),
                    'image_url': None,
                    'session_id': session_id
                }
                
                # Generate image
                image_url = openai_service.generate_image(answer)
                if image_url:
                    card['image_url'] = image_url
                
                # Save card to database
                save_card(db, card, session_id)
                
                # Update context
                session['context'].update({
                    'memories': answer,
                    'stage': 'complete'
                })
                session['stage'] = 'complete'
            
            # Get next question
            question = openai_service.get_next_question({
                'stage': session['stage'],
                'context': session['context']
            })
            
            response = jsonify({
                'success': True,
                'question': question,
                'stage': session['stage']
            })
            
            # Set session cookie
            response.set_cookie('session', session_id)
            return response
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in submit_answer: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

def create_card_from_answer(answer: str, question: str, stage: str) -> dict:
    """Create a card from the answer data."""
    try:
        # Determine card type based on question content and answer
        card_type = 'memory'  # Default type
        
        # Check for place indicators
        if ('born' in answer.lower() or 'grew up' in answer.lower() or 
            'lived' in answer.lower() or 'city' in answer.lower() or
            'town' in answer.lower() or 'country' in answer.lower()):
            card_type = 'place'
            
        # Check for person indicators
        elif ('mother' in answer.lower() or 'father' in answer.lower() or
              'parent' in answer.lower() or 'sister' in answer.lower() or
              'brother' in answer.lower() or 'family member' in answer.lower()):
            card_type = 'person'
            
        # Check for event indicators
        elif ('graduated' in answer.lower() or 'wedding' in answer.lower() or
              'birthday' in answer.lower() or 'ceremony' in answer.lower() or
              any(year in answer for year in [str(y) for y in range(1900, 2100)])):
            card_type = 'event'
            
        # Create the card
        card = {
            'id': str(uuid.uuid4()),
            'type': card_type,
            'title': question,
            'description': answer,
            'date': datetime.now().isoformat(),  # Store as ISO format string
            'session_id': request.cookies.get('session'),
            'created_at': datetime.now().isoformat()  # Store as ISO format string
        }
        
        # Add type-specific fields
        if card_type == 'place':
            # Extract location from answer
            location_match = re.search(r'(?:in|from|at)\s+([^\.]+)', answer)
            if location_match:
                location = location_match.group(1).strip()
            else:
                location = answer.split('.')[0].strip()
            card['location'] = location
            
        elif card_type == 'person':
            # Extract people from answer
            people = []
            if 'mother' in answer.lower():
                people.append('mother')
            if 'father' in answer.lower():
                people.append('father')
            if 'sister' in answer.lower():
                people.append('sister')
            if 'brother' in answer.lower():
                people.append('brother')
            card['people'] = people
            
        elif card_type == 'event':
            # Extract date from answer
            date_match = re.search(r'\b\d{4}\b', answer)
            if date_match:
                year = int(date_match.group(0))
                card['date'] = datetime(year, 1, 1).isoformat()  # Store as ISO format string
            
        # Generate image
        image_prompt = f"A beautiful, artistic representation of {answer}. {question}"
        image_url = openai_service.generate_image(image_prompt)
        if image_url:
            card['image_url'] = image_url
        else:
            # Fallback image URL for testing
            card['image_url'] = 'https://example.com/placeholder.jpg'
            
        return card
        
    except Exception as e:
        logger.error(f"Error creating card: {str(e)}")
        return None

@interview_bp.route('/interview/process', methods=['POST'], strict_slashes=False)
def process_response():
    """Process interview responses and create cards."""
    try:
        # Check if request has JSON content type
        if not request.is_json:
            return jsonify({
                "error": "Request must have application/json content type"
            }), 400
        
        # Try to parse JSON data
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({
                "error": "Invalid JSON format",
                "details": str(e)
            }), 400
        
        # Validate required fields
        if not data:
            return jsonify({
                "error": "Empty request body"
            }), 400
            
        if 'response' not in data:
            return jsonify({
                "error": "Missing required field: response"
            }), 400
            
        response = data['response']
        
        # Validate response type
        valid_types = {'memory', 'people', 'location'}
        response_type = next((t for t in valid_types if t in response), None)
        
        if not response_type:
            return jsonify({
                "error": "Unsupported response type",
                "valid_types": list(valid_types)
            }), 400
        
        # Process different types of responses
        try:
            if response_type == 'memory':
                memory = response['memory']
                if not memory.get('title') or not memory.get('description'):
                    return jsonify({
                        "error": "Memory requires title and description"
                    }), 400
                card = MemoryCard(
                    title=memory['title'],
                    description=memory['description'],
                    created_at=datetime.now()
                )
            elif response_type == 'people':
                person = response['people'][0]  # Assuming single person for now
                if not person.get('title') or not person.get('description'):
                    return jsonify({
                        "error": "Person requires title and description"
                    }), 400
                card = PersonCard(
                    title=person['title'],
                    description=person['description'],
                    created_at=datetime.now()
                )
            else:  # location
                location = response['location']
                if not location.get('title') or not location.get('description'):
                    return jsonify({
                        "error": "Location requires title and description"
                    }), 400
                card = PlaceCard(
                    title=location['title'],
                    description=location['description'],
                    latitude=location.get('latitude', 0),
                    longitude=location.get('longitude', 0),
                    created_at=datetime.now()
                )
        except Exception as e:
            return jsonify({
                "error": "Card initialization error",
                "details": str(e)
            }), 400
        
        # Save the card
        try:
            card_id = save_card(card)
            return jsonify({
                "success": True,
                "message": "Card saved successfully",
                "card_id": card_id
            })
        except DatabaseError as e:
            logger.error(f"Database error saving card: {str(e)}")
            return jsonify({
                "error": "Database error",
                "details": str(e)
            }), 500
            
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

def generate_ai_question(answers: List[Dict]) -> str:
    """Generate a context-aware question based on previous answers."""
    try:
        # Extract key information from answers
        context = []
        for answer in answers:
            context.append(f"Q: {answer['question']}\nA: {answer['answer']}")
        
        # Generate a follow-up question based on the context
        # This is a simplified version - in reality, you'd use an AI model
        if len(answers) > 0:
            last_answer = answers[-1]
            if 'parents' in last_answer['question'].lower():
                return "How did your relationship with your parents affect your childhood?"
            elif 'siblings' in last_answer['question'].lower():
                return "What are some specific memories you have with your siblings?"
            elif 'place' in last_answer['question'].lower():
                return "What was your favorite thing about growing up there?"
        
        return "Can you tell me more about that?"
    except Exception as e:
        logger.error(f"Error generating AI question: {str(e)}")
        return "Can you tell me more about that?"

@interview_bp.route('/timeline', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_timeline():
    """Get timeline data for the current session."""
    try:
        logger.info("GET /timeline called")
        
        # Get session ID from request
        session_id = request.cookies.get('session')
        if not session_id:
            return jsonify({
                "error": "No session found",
                "details": "Please start an interview first"
            }), 400
        
        # Get session data
        session_data = session_db.get_session(session_id)
        if not session_data:
            return jsonify({
                "error": "Invalid session",
                "details": "Session not found"
            }), 400
            
        # Get interview stage
        if 'interview_stage' not in session_data:
            return jsonify({
                "error": "No interview data",
                "details": "Please complete the interview first"
            }), 400
            
        stage = InterviewStage.from_dict(session_data['interview_stage'])
        
        # Format timeline data
        timeline_data = []
        for answer in stage.answers:
            # Create a card for each answer
            card = create_card_from_answer(
                answer['answer'],
                answer['question'],
                answer['stage']
            )
            if card:
                timeline_data.append(card)
            
        return jsonify({
            "success": True,
            "timeline": timeline_data
        })
        
    except Exception as e:
        logger.error(f"Error getting timeline: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

def extract_people(answer: str) -> List[str]:
    """Extract people from answer text."""
    people = []
    
    # Look for common people patterns
    people_patterns = [
        r'my (mother|father|mom|dad|sister|brother|sibling|parent)',
        r'my (grandmother|grandfather|grandma|grandpa)',
        r'my (aunt|uncle|cousin)',
        r'my (wife|husband|spouse|partner)',
        r'my (son|daughter|child|kid)'
    ]
    
    for pattern in people_patterns:
        match = re.search(pattern, answer.lower())
        if match:
            people.append(match.group(1))
    
    # If no patterns match, return empty list
    return people

def extract_date(answer: str) -> Optional[datetime]:
    """Extract date from answer text."""
    # Look for year pattern
    year_match = re.search(r'\b(19|20)\d{2}\b', answer)
    if year_match:
        year = int(year_match.group(0))
        return datetime(year, 1, 1)  # Default to January 1st of the year
    
    # Look for month and year pattern
    month_year_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', answer)
    if month_year_match:
        month = month_year_match.group(1)
        year = int(month_year_match.group(2))
        month_num = datetime.strptime(month, '%B').month
        return datetime(year, month_num, 1)  # Default to 1st of the month
    
    # Look for full date pattern
    date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', answer)
    if date_match:
        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3))
        return datetime(year, month, day)
    
    # If no patterns match, return None
    return None