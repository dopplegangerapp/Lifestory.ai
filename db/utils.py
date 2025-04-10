from typing import Union
from .models import (
    BaseModel,
    EventModel,
    LocationModel, 
    PersonModel,
    EmotionModel
)
from . import SessionLocal
from cards.base_card import BaseCard
from cards.event_card import EventCard
from cards.location_card import LocationCard
from cards.person_card import PersonCard
from cards.emotion_card import EmotionCard

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

def save_card(card: Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard]):
    """Save card to database"""
    db = SessionLocal()
    try:
        model = card_to_model(card)
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    finally:
        db.close()
