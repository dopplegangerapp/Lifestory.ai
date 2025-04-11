import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure database
app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev-secret-key'),
    SESSION_COOKIE_SECURE=False,  # Allow HTTP in development
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    TESTING=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///instance/droecore.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
app.url_map.strict_slashes = False

db = SQLAlchemy(app)

# Import and register routes
from routes.card_viewer import card_viewer_bp
from routes.timeline import timeline_bp
from routes.interview import interview_bp
from routes.media import bp as media_bp

# Register blueprints
app.register_blueprint(timeline_bp, url_prefix='/timeline')
app.register_blueprint(card_viewer_bp, url_prefix='/cards')
app.register_blueprint(interview_bp, url_prefix='/interview')
app.register_blueprint(media_bp, url_prefix='/media')

@app.route('/')
def index():
    return "DroeCore API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
