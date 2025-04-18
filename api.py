from flask import Flask, jsonify, request, session, make_response
from flask_cors import CORS
from flask_session import Session
from db import SessionLocal
from db.utils import save_card, card_to_model, get_cards_for_session, get_timeline_for_session
from db.init_db import init_db
from cards.event_card import EventCard
from cards.location_card import LocationCard
from cards.person_card import PersonCard
from cards.emotion_card import EmotionCard
from routes.interview import interview_bp
from routes.timeline import timeline_bp
from routes.cards import cards_bp
import uuid
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')
app.config['SESSION_FILE_THRESHOLD'] = 100

# Create session directory if it doesn't exist
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# Initialize Flask-Session
Session(app)

# Initialize database
init_db()

CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:8501"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Register blueprints
app.register_blueprint(interview_bp)
app.register_blueprint(timeline_bp)
app.register_blueprint(cards_bp)

# Database middleware
@app.before_request
def get_db():
    request.db = SessionLocal()

@app.teardown_request
def close_db(exception=None):
    db = getattr(request, 'db', None)
    if db is not None:
        db.close()

# Cards endpoint
@app.route('/cards', methods=['GET'])
def get_cards():
    """Get all cards for the current session."""
    try:
        # Get session ID from request
        session_id = request.cookies.get('session')
        if not session_id:
            return jsonify({
                "error": "No session cookie found"
            }), 401
        
        # Get cards from database
        cards = get_cards_for_session(request.db, session_id)
        return jsonify({
            "success": True,
            "cards": [card_to_model(card) for card in cards]
        })
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

# Timeline endpoint
@app.route('/timeline', methods=['GET'])
def get_timeline():
    """Get timeline items for the current session."""
    try:
        # Get session ID from request
        session_id = request.cookies.get('session')
        if not session_id:
            return jsonify({
                "error": "No session cookie found"
            }), 401
        
        # Get timeline from database
        timeline = get_timeline_for_session(request.db, session_id)
        return jsonify({
            "success": True,
            "timeline": [card_to_model(card) for card in timeline]
        })
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Enable debug mode for development
