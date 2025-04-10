from datetime import datetime
from typing import List, Dict
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """Base database model with common fields"""
    __abstract__ = True
    id = Column(String, primary_key=True)
    created_at = Column(Integer, default=lambda: int(datetime.now().timestamp()))
    updated_at = Column(Integer, onupdate=lambda: int(datetime.now().timestamp()))
    image_path = Column(String)

class EventModel(BaseModel):
    """Database model for Event cards"""
    __tablename__ = 'events'
    title = Column(String)
    description = Column(String)
    location_data = Column(JSON)  # {'id': 'loc123', 'name': 'Home'}
    people_data = Column(JSON)    # [{'id': 'person1', 'name': 'John'}]
    emotions_data = Column(JSON)  # [{'id': 'happy', 'name': 'Happy'}]
    memories_data = Column(JSON)  # [{'id': 'mem1', 'name': 'Birthday'}]

class LocationModel(BaseModel):
    """Database model for Location cards"""
    __tablename__ = 'locations'
    name = Column(String)
    description = Column(String)
    events_data = Column(JSON)  # [{'id': 'event1', 'name': 'Birthday Party'}]
    memories_data = Column(JSON)  # [{'id': 'mem1', 'name': 'Childhood Home'}]

class PersonModel(BaseModel):
    """Database model for Person cards"""
    __tablename__ = 'people'
    name = Column(String)
    relationship = Column(String)
    description = Column(String)
    events_data = Column(JSON)  # [{'id': 'event1', 'name': 'Birthday Party'}]
    memories_data = Column(JSON)  # [{'id': 'mem1', 'name': 'Childhood Friend'}]

class EmotionModel(BaseModel):
    """Database model for Emotion cards"""
    __tablename__ = 'emotions'
    name = Column(String)
    intensity = Column(String)
    memories_data = Column(JSON)  # [{'id': 'mem1', 'name': 'Graduation Day'}]
