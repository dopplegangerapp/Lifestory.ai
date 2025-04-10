from flask import Blueprint, render_template, jsonify
from datetime import datetime
from typing import Dict, Any, List
from utils.db_utils import get_db

timeline_bp = Blueprint('timeline', __name__)

@timeline_bp.route('/')
def timeline():
    """Render the timeline view."""
    return render_template('timeline.html')

@timeline_bp.route('/events')
def get_events():
    """Get all events and memories for the timeline."""
    db = get_db()
    events = db.execute('''
        SELECT id, title, description, date, 'event' as type, location_id, created_at
        FROM events
        UNION ALL
        SELECT id, title, description, date, 'memory' as type, NULL as location_id, created_at
        FROM memories
        ORDER BY date DESC
    ''').fetchall()
    
    return jsonify([dict(event) for event in events])

@timeline_bp.route('/event/<int:event_id>')
def get_event_details(event_id: int):
    """Get detailed information about a specific event."""
    db = get_db()
    
    # Get event details
    event = db.execute('''
        SELECT e.*, l.name as location_name
        FROM events e
        LEFT JOIN locations l ON e.location_id = l.id
        WHERE e.id = ?
    ''', (event_id,)).fetchone()
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Get associated people
    people = db.execute('''
        SELECT p.*
        FROM people p
        JOIN event_people ep ON p.id = ep.person_id
        WHERE ep.event_id = ?
    ''', (event_id,)).fetchall()
    
    # Get associated media
    media = db.execute('''
        SELECT *
        FROM media
        WHERE event_id = ?
    ''', (event_id,)).fetchall()
    
    return jsonify({
        "event": dict(event),
        "people": [dict(person) for person in people],
        "media": [dict(item) for item in media]
    })

@timeline_bp.route('/memory/<int:memory_id>')
def get_memory_details(memory_id: int):
    """Get detailed information about a specific memory."""
    db = get_db()
    
    # Get memory details
    memory = db.execute('SELECT * FROM memories WHERE id = ?', (memory_id,)).fetchone()
    
    if not memory:
        return jsonify({"error": "Memory not found"}), 404
    
    # Get associated media
    media = db.execute('''
        SELECT *
        FROM media
        WHERE memory_id = ?
    ''', (memory_id,)).fetchall()
    
    return jsonify({
        "memory": dict(memory),
        "media": [dict(item) for item in media]
    })
