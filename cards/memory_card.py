from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from .base_card import BaseCard
from .event_card import EventCard
from .person_card import PersonCard
from .place_card import PlaceCard
from .time_period_card import TimePeriodCard

@dataclass
class MemoryCard(BaseCard):
    """Card representing a memory in the DROE Core system."""
    
    # Required fields from BaseCard
    title: str
    description: str
    
    # Optional fields from BaseCard
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    metadata: Optional[dict] = None
    image_path: str = ""
    media: List['Media'] = field(default_factory=list)
    
    # Memory-specific fields
    date: Optional[datetime] = None
    location: Optional[str] = None
    people: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    media_ids: List[str] = field(default_factory=list)
    
    def __init__(self,
                 title: str,
                 description: str,
                 date: Optional[datetime] = None,
                 location: Optional[str] = None,
                 people: Optional[List[str]] = None,
                 emotions: Optional[List[str]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 id: Optional[str] = None,
                 created_by: Optional[str] = None,
                 media_ids: Optional[List[str]] = None):
        """
        Initialize a memory card.
        
        Args:
            title (str): Memory's title
            description (str): Memory's description
            date (datetime, optional): When the memory occurred
            location (str, optional): Where the memory occurred
            people (List[str], optional): People involved in the memory
            emotions (List[str], optional): Emotions associated with the memory
            created_at (datetime, optional): When the card was created
            updated_at (datetime, optional): When the card was last updated
            id (str, optional): ID of the card
            created_by (str, optional): Who created the card
            media_ids (List[str], optional): IDs of associated media
        """
        super().__init__(title=title, description=description, id=id)
        self.date = date
        self.location = location
        self.people = people or []
        self.emotions = emotions or []
        self.created_by = created_by
        self.media_ids = media_ids or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def set_event(self, event: 'EventCard') -> None:
        """Set the associated event."""
        self.associated_event = event
        self.updated_at = datetime.now()
    
    def add_person(self, person: 'PersonCard') -> None:
        """Add a person to the memory."""
        if person not in self.associated_people:
            self.associated_people.append(person)
            self.updated_at = datetime.now()
    
    def set_place(self, place: 'PlaceCard') -> None:
        """Set the associated place."""
        self.associated_place = place
        self.updated_at = datetime.now()
    
    def set_time_period(self, time_period: 'TimePeriodCard') -> None:
        """Set the associated time period."""
        self.associated_time_period = time_period
        self.updated_at = datetime.now()
    
    def set_emotion(self, emotion: str, intensity: int) -> None:
        """Set the emotion and its intensity."""
        self.emotion = emotion
        self.intensity = max(0, min(10, intensity))  # Ensure intensity is between 0 and 10
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the memory to a dictionary."""
        data = super().to_dict()
        data.update({
            'date': self.date.isoformat(),
            'associated_event': self.associated_event.to_dict() if self.associated_event else None,
            'associated_people': [p.to_dict() for p in self.associated_people],
            'associated_place': self.associated_place.to_dict() if self.associated_place else None,
            'associated_time_period': self.associated_time_period.to_dict() if self.associated_time_period else None,
            'emotion': self.emotion,
            'intensity': self.intensity
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryCard':
        """Create a memory from a dictionary."""
        from .event_card import EventCard
        from .person_card import PersonCard
        from .place_card import PlaceCard
        from .time_period_card import TimePeriodCard
        
        # Create memory card
        memory = cls(
            title=data['title'],
            description=data['description'],
            id=data.get('id'),
            date=datetime.fromisoformat(data['date']) if 'date' in data else None
        )
        
        # Set base card attributes
        memory.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        memory.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        memory.metadata = data.get('metadata', {})
        memory.image_path = data.get('image_path', '')
        
        # Set memory-specific attributes
        memory.associated_event = EventCard.from_dict(data['associated_event']) if data.get('associated_event') else None
        memory.associated_people = [PersonCard.from_dict(p) for p in data.get('associated_people', [])]
        memory.associated_place = PlaceCard.from_dict(data['associated_place']) if data.get('associated_place') else None
        memory.associated_time_period = TimePeriodCard.from_dict(data['associated_time_period']) if data.get('associated_time_period') else None
        memory.emotion = data.get('emotion')
        memory.intensity = data.get('intensity')
        
        return memory 