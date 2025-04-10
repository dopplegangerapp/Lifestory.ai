from flask import Flask
from .card_viewer import card_viewer_bp
from .timeline import timeline_bp
from .interview import interview_bp
from .media import bp as media_bp

def register_routes(app: Flask):
    """Register all route blueprints with the Flask application."""
    app.register_blueprint(timeline_bp)
    app.register_blueprint(card_viewer_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(media_bp) 