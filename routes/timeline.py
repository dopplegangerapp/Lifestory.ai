from flask import Blueprint, render_template, jsonify, request, session
from flask_cors import cross_origin
from datetime import datetime
from typing import Dict, Any, List, Optional
from db import SessionLocal
from db.models import Card
from sqlalchemy import desc
from db.utils import get_timeline_for_session, card_to_model
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

timeline_bp = Blueprint('timeline', __name__)

def parse_date(date_str: str) -> str:
    """Parse a date string and return ISO format."""
    if not date_str:
        return None
    
    # If it's already a datetime object, convert to ISO format
    if isinstance(date_str, datetime):
        return date_str.isoformat()
    
    # If it's a timestamp (integer), convert to ISO format
    if isinstance(date_str, int):
        return datetime.fromtimestamp(date_str).isoformat()
    
    try:
        # Try parsing as ISO format first
        dt = datetime.fromisoformat(str(date_str))
    except ValueError:
        try:
            # Try parsing RFC format
            dt = datetime.strptime(str(date_str), '%a, %d %b %Y %H:%M:%S GMT')
        except ValueError:
            try:
                # Try parsing other common formats
                dt = datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    # Try parsing date only format
                    dt = datetime.strptime(str(date_str), '%Y-%m-%d')
                except ValueError:
                    # Return original string if parsing fails
                    return str(date_str)
    return dt.isoformat()

@timeline_bp.route('/timeline', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_timeline():
    """Get the timeline for the current session."""
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
            # Get timeline items
            timeline_items = get_timeline_for_session(db, session_id)
            
            # Format timeline items
            formatted_items = []
            for item in timeline_items:
                formatted_item = card_to_model(item)
                if formatted_item.get('date'):
                    formatted_item['date'] = parse_date(formatted_item['date'])
                formatted_items.append(formatted_item)
            
            # Sort items by date
            formatted_items.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            # Return empty timeline if no items found
            return jsonify({
                "success": True,
                "timeline": formatted_items
            })
            
        finally:
            # Close database session
            db.close()
            
    except Exception as e:
        logger.error(f"Error in get_timeline: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@timeline_bp.route('/event/<string:card_id>')
@cross_origin(supports_credentials=True)
def get_event_details(card_id: str):
    """Get detailed information about a specific event."""
    db = SessionLocal()
    try:
        # Get card details
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            return jsonify({"error": "Event not found"}), 404
        
        # Convert card to event details
        event_dict = {
            'id': card.id,
            'type': card.type,
            'title': card.title,
            'description': card.description,
            'date': parse_date(card.date),
            'created_at': parse_date(card.created_at),
            'image_url': card.image_url
        }
        
        # Add type-specific fields
        if card.type == 'place':
            event_dict['location'] = card.location
        elif card.type == 'person':
            event_dict['people'] = card.people
        elif card.type == 'emotion':
            event_dict['emotions'] = card.emotions
            
        return jsonify({"event": event_dict})
    finally:
        db.close()

@timeline_bp.route('/memory/<string:card_id>')
@cross_origin(supports_credentials=True)
def get_memory_details(card_id: str):
    """Get detailed information about a specific memory."""
    db = SessionLocal()
    try:
        # Get card details
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            return jsonify({"error": "Memory not found"}), 404
        
        # Convert card to memory details
        memory_dict = {
            'id': card.id,
            'type': card.type,
            'title': card.title,
            'description': card.description,
            'date': parse_date(card.date),
            'created_at': parse_date(card.created_at),
            'image_url': card.image_url
        }
        
        # Add type-specific fields
        if card.type == 'place':
            memory_dict['location'] = card.location
        elif card.type == 'person':
            memory_dict['people'] = card.people
        elif card.type == 'emotion':
            memory_dict['emotions'] = card.emotions
            
        return jsonify({"memory": memory_dict})
    finally:
        db.close()
