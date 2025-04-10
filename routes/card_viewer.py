from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for
from datetime import datetime
import uuid
from typing import Dict, List
from utils.db_utils import get_db

# Create the blueprint
card_viewer_bp = Blueprint('card_viewer_bp', __name__, url_prefix='/cards')

@card_viewer_bp.route('/person/<id>')
def view_person(id):
    """View details for a specific person"""
    db = get_db()
    person = db.execute('SELECT * FROM people WHERE id = ?', (id,)).fetchone()
    if not person:
        abort(404)
    return render_template('person_view.html', person=person)

@card_viewer_bp.route('/place/<id>')
def view_place(id):
    """View details for a specific place"""
    db = get_db()
    place = db.execute('SELECT * FROM places WHERE id = ?', (id,)).fetchone()
    if not place:
        abort(404)
    return render_template('place_view.html', place=place)

@card_viewer_bp.route('/event/<id>')
def view_event(id):
    """View details for a specific event"""
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    if not event:
        abort(404)
    return render_template('event_view.html', event=event)

@card_viewer_bp.route('/time/<year>')
def view_time(year):
    """View events from a specific year"""
    db = get_db()
    events = db.execute('''
        SELECT * FROM events 
        WHERE strftime('%Y', date) = ?
        ORDER BY date
    ''', (year,)).fetchall()
    return render_template('time.html', year=year, events=events)

@card_viewer_bp.route('/people')
def people():
    """List all people"""
    db = get_db()
    people = db.execute('SELECT * FROM people ORDER BY name').fetchall()
    return render_template('people_list.html', people=people)

@card_viewer_bp.route('/places')
def places():
    """List all places"""
    db = get_db()
    places = db.execute('SELECT * FROM places ORDER BY name').fetchall()
    return render_template('places_list.html', places=places)

@card_viewer_bp.route('/events')
def events():
    """List all events"""
    db = get_db()
    events = db.execute('SELECT * FROM events ORDER BY start_date').fetchall()
    return render_template('events_list.html', events=events)

@card_viewer_bp.route('/emotions')
def emotions():
    """List all emotions"""
    db = get_db()
    emotions = db.execute('''
        SELECT DISTINCT m.id, m.title, m.description, m.created_at
        FROM memories m
        WHERE m.description LIKE '%feel%' OR m.description LIKE '%emotion%'
        ORDER BY m.created_at DESC
    ''').fetchall()
    return render_template('emotions_list.html', emotions=emotions)

@card_viewer_bp.route('/person/add', methods=['GET', 'POST'])
def add_person():
    """Add a new person"""
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO people (name, relationship, description, created_by)
            VALUES (?, ?, ?, ?)
        ''', (
            request.form['name'],
            request.form['relationship'],
            request.form.get('description', ''),
            1  # Default user_id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.people'))
    return render_template('person_form.html')

@card_viewer_bp.route('/person/<id>/edit', methods=['GET', 'POST'])
def edit_person(id):
    """Edit an existing person"""
    db = get_db()
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute('''
            UPDATE people 
            SET name = ?, relationship = ?, image_path = ?, events_data = ?, memories_data = ?
            WHERE id = ?
        ''', (
            request.form['name'],
            request.form['relationship'],
            request.form.get('image_path', ''),
            request.form.get('events_data', '[]'),
            request.form.get('memories_data', '[]'),
            id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.view_person', id=id))
    
    person = db.execute('SELECT * FROM people WHERE id = ?', (id,)).fetchone()
    if not person:
        abort(404)
    return render_template('edit_person.html', person=person)

@card_viewer_bp.route('/place/add', methods=['GET', 'POST'])
def add_place():
    """Add a new place"""
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO places (name, description, latitude, longitude, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            request.form['name'],
            request.form.get('description', ''),
            request.form.get('latitude', None),
            request.form.get('longitude', None),
            1  # Default user_id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.places'))
    return render_template('place_form.html')

@card_viewer_bp.route('/place/<id>/edit', methods=['GET', 'POST'])
def edit_place(id):
    """Edit an existing place"""
    db = get_db()
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute('''
            UPDATE places 
            SET name = ?, description = ?, latitude = ?, longitude = ?
            WHERE id = ?
        ''', (
            request.form['name'],
            request.form.get('description', ''),
            request.form.get('latitude', None),
            request.form.get('longitude', None),
            id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.view_place', id=id))
    
    place = db.execute('SELECT * FROM places WHERE id = ?', (id,)).fetchone()
    if not place:
        abort(404)
    return render_template('edit_place.html', place=place)

@card_viewer_bp.route('/event/add', methods=['GET', 'POST'])
def add_event():
    """Add a new event"""
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO events (title, description, start_date, end_date, location_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.form['title'],
            request.form['description'],
            request.form['start_date'],
            request.form.get('end_date'),
            request.form.get('location_id'),
            1  # Default user_id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.events'))
    return render_template('event_form.html')

@card_viewer_bp.route('/event/<id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    """Edit an existing event"""
    db = get_db()
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute('''
            UPDATE events 
            SET title = ?, description = ?, date = ?, image_path = ?, location_id = ?,
                people_data = ?, emotions_data = ?, memories_data = ?
            WHERE id = ?
        ''', (
            request.form['title'],
            request.form['description'],
            request.form['date'],
            request.form.get('image_path', ''),
            request.form.get('location_id', ''),
            request.form.get('people_data', '[]'),
            request.form.get('emotions_data', '[]'),
            request.form.get('memories_data', '[]'),
            id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.view_event', id=id))
    
    event = db.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    if not event:
        abort(404)
    return render_template('edit_event.html', event=event)

@card_viewer_bp.route('/emotion/add', methods=['GET', 'POST'])
def add_emotion():
    """Add a new emotion"""
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO emotions (id, name, intensity, image_path, memories_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            request.form['name'],
            request.form['intensity'],
            request.form.get('image_path', ''),
            request.form.get('memories_data', '[]'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.emotions'))
    return render_template('add_emotion.html')

@card_viewer_bp.route('/emotion/<id>/edit', methods=['GET', 'POST'])
def edit_emotion(id):
    """Edit an existing emotion"""
    db = get_db()
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute('''
            UPDATE emotions 
            SET name = ?, intensity = ?, image_path = ?, memories_data = ?
            WHERE id = ?
        ''', (
            request.form['name'],
            request.form['intensity'],
            request.form.get('image_path', ''),
            request.form.get('memories_data', '[]'),
            id
        ))
        db.commit()
        return redirect(url_for('card_viewer_bp.view_emotion', id=id))
    
    emotion = db.execute('SELECT * FROM emotions WHERE id = ?', (id,)).fetchone()
    if not emotion:
        abort(404)
    return render_template('edit_emotion.html', emotion=emotion)

@card_viewer_bp.route('/emotion/<id>')
def view_emotion(id):
    """View details for a specific emotion"""
    db = get_db()
    emotion = db.execute('SELECT * FROM emotions WHERE id = ?', (id,)).fetchone()
    if not emotion:
        abort(404)
    return render_template('emotion.html', emotion=emotion) 