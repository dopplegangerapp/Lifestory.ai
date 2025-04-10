from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from ai.image_generator import ImageGenerator, ImageGenerationError
from utils.db_utils import get_db
import uuid

bp = Blueprint('media', __name__, url_prefix='/media')

# Configure upload folder
UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_media_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in {'png', 'jpg', 'jpeg', 'gif'}:
        return 'image'
    elif ext in {'mp4'}:
        return 'video'
    elif ext in {'mp3', 'wav'}:
        return 'audio'
    return 'document'

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = secure_filename(f"{timestamp}_{unique_id}_{file.filename}")
            
            # Create user-specific directory if it doesn't exist
            user_id = request.form.get('user_id', 'default')
            user_dir = os.path.join(UPLOAD_FOLDER, user_id)
            os.makedirs(user_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(user_dir, filename)
            file.save(file_path)
            
            # Save to database
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO media (file_path, type, description, created_at) VALUES (?, ?, ?, ?)',
                (file_path, get_media_type(filename), request.form.get('description', ''), datetime.now())
            )
            db.commit()
            
            return jsonify({
                'message': 'File uploaded successfully',
                'file_path': file_path,
                'media_id': cursor.lastrowid
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Initialize image generator
        image_generator = ImageGenerator()
        
        # Generate image
        image_url, error = image_generator.generate_image(data['prompt'])
        if error:
            return jsonify({'error': error}), 400
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO media (file_path, type, description, created_at) VALUES (?, ?, ?, ?)',
            (image_url, 'image', data.get('description', ''), datetime.now())
        )
        db.commit()
        
        return jsonify({
            'message': 'Image generated successfully',
            'image_url': image_url,
            'media_id': cursor.lastrowid
        })
    
    except ImageGenerationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<path:filename>')
def serve_media(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/<int:media_id>')
def get_media(media_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM media WHERE id = ?', (media_id,))
        media = cursor.fetchone()
        
        if media is None:
            return jsonify({'error': 'Media not found'}), 404
        
        return jsonify({
            'id': media['id'],
            'file_path': media['file_path'],
            'type': media['type'],
            'description': media['description'],
            'created_at': media['created_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 