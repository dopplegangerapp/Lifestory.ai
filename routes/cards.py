from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from db import SessionLocal
from db.utils import get_cards_for_session, card_to_model
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/cards', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_cards():
    """Get all cards for the current session."""
    try:
        # Get session ID from cookie
        session_id = request.cookies.get('session')
        if not session_id:
            return jsonify({
                "error": "No session cookie found"
            }), 401
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Get cards
            cards = get_cards_for_session(db, session_id)
            
            # Format cards
            formatted_cards = [card_to_model(card) for card in cards]
            
            return jsonify({
                "success": True,
                "cards": formatted_cards
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in get_cards: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500 