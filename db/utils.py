from typing import Union, List
from .models import (
    BaseModel,
    EventModel,
    LocationModel, 
    PersonModel,
    EmotionModel,
    Card
)
from . import SessionLocal
from cards.base_card import BaseCard
from cards.event_card import EventCard
from cards.location_card import LocationCard
from cards.person_card import PersonCard
from cards.emotion_card import EmotionCard
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

def card_to_model(card: Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard]) -> BaseModel:
    """Convert card object to database model"""
    if isinstance(card, EventCard):
        return EventModel(
            id=card.id,
            image_path=card.image_path,
            title=card.title,
            description=card.description,
            location_data=card.location,
            people_data=card.people,
            emotions_data=card.emotions,
            memories_data=card.memories
        )
    elif isinstance(card, LocationCard):
        return LocationModel(
            id=card.id,
            image_path=card.image_path,
            name=card.name,
            events_data=card.events,
            memories_data=card.memories
        )
    elif isinstance(card, PersonCard):
        return PersonModel(
            id=card.id,
            image_path=card.image_path,
            name=card.name,
            relationship=card.relationship,
            events_data=card.events,
            memories_data=card.memories
        )
    elif isinstance(card, EmotionCard):
        return EmotionModel(
            id=card.id,
            image_path=card.image_path,
            name=card.name,
            intensity=card.intensity,
            memories_data=card.memories
        )
    else:
        raise ValueError(f"Unsupported card type: {type(card)}")

def model_to_card(model: BaseModel) -> Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard]:
    """Convert database model to card object"""
    if isinstance(model, EventModel):
        return EventCard(
            id=model.id,
            image_path=model.image_path,
            title=model.title,
            description=model.description,
            location=model.location_data,
            people=model.people_data,
            emotions=model.emotions_data,
            memories=model.memories_data
        )
    elif isinstance(model, LocationModel):
        return LocationCard(
            id=model.id,
            image_path=model.image_path,
            name=model.name,
            events=model.events_data,
            memories=model.memories_data
        )
    elif isinstance(model, PersonModel):
        return PersonCard(
            id=model.id,
            image_path=model.image_path,
            name=model.name,
            relationship=model.relationship,
            events=model.events_data,
            memories=model.memories_data
        )
    elif isinstance(model, EmotionModel):
        return EmotionCard(
            id=model.id,
            image_path=model.image_path,
            name=model.name,
            intensity=model.intensity,
            memories=model.memories_data
        )
    else:
        raise ValueError(f"Unsupported model type: {type(model)}")

def save_card(db: Session, card: dict, session_id: str) -> Card:
    """Save a card to the database."""
    # Convert date string to datetime if provided
    date = None
    if card.get('date'):
        try:
            date = datetime.fromisoformat(card['date'].replace('Z', '+00:00'))
        except ValueError:
            try:
                date = datetime.strptime(card['date'], '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                date = None
    
    db_card = Card(
        id=card.get('id'),
        type=card.get('type'),
        title=card.get('title'),
        description=card.get('description'),
        date=date,
        image_url=card.get('image_url'),
        session_id=session_id,
        created_at=datetime.now(),
        location=card.get('location'),
        people=card.get('people'),
        emotions=card.get('emotions')
    )
    
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def card_to_model(card: Card) -> dict:
    """Convert a database card to a dictionary."""
    return {
        'id': card.id,
        'type': card.type,
        'title': card.title,
        'description': card.description,
        'date': card.date.isoformat() if card.date else None,
        'image_url': card.image_url,
        'session_id': card.session_id,
        'created_at': card.created_at.isoformat(),
        'location': card.location,
        'people': card.people,
        'emotions': card.emotions
    }

def get_cards_for_session(db: Session, session_id: str) -> List[Card]:
    """Get all cards for a session."""
    return db.query(Card).filter(Card.session_id == session_id).all()

def get_timeline_for_session(db: Session, session_id: str) -> List[Card]:
    """Get timeline items for a session, ordered by date."""
    return db.query(Card).filter(
        Card.session_id == session_id,
        Card.date.isnot(None)
    ).order_by(desc(Card.date)).all()
