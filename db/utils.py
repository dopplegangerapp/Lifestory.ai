from typing import Union, List
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

def save_card(card: Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard], db_session=None):
    """Save card to database"""
    close_session = False
    if db_session is None:
        db_session = SessionLocal()
        close_session = True
    try:
        model = card_to_model(card)
        db_session.add(model)
        db_session.commit()
        db_session.refresh(model)
        return model
    finally:
        if close_session:
            db_session.close()

def get_all_cards(db_session=None) -> List[Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard]]:
    """Get all cards from database"""
    close_session = False
    if db_session is None:
        db_session = SessionLocal()
        close_session = True
    try:
        # Get all models
        event_cards = db_session.query(EventModel).all()
        location_cards = db_session.query(LocationModel).all()
        person_cards = db_session.query(PersonModel).all()
        emotion_cards = db_session.query(EmotionModel).all()
        
        # Convert models to cards
        cards = []
        for model in event_cards + location_cards + person_cards + emotion_cards:
            try:
                card = model_to_card(model)
                cards.append(card)
            except Exception as e:
                print(f"Error converting model to card: {str(e)}")
                continue
        
        return cards
    finally:
        if close_session:
            db_session.close()
