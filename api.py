from flask import Flask, jsonify, request
from db import SessionLocal
from db.utils import save_card, card_to_model
from cards.event_card import EventCard
from cards.location_card import LocationCard
from cards.person_card import PersonCard
from cards.emotion_card import EmotionCard
import uuid

app = Flask(__name__)

# Database middleware
@app.before_request
def get_db():
    request.db = SessionLocal()

@app.teardown_request
def close_db(exception=None):
    db = getattr(request, 'db', None)
    if db is not None:
        db.close()

# [Keep all existing API endpoints but remove template routes]

if __name__ == '__main__':
    app.run(port=5000)  # API on port 5000
