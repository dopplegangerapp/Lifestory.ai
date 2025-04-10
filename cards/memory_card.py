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
    
    date: datetime = field(default_factory=datetime.now)
    associated_event: Optional['EventCard'] = None
    associated_people: List['PersonCard'] = field(default_factory=list)
    associated_place: Optional['PlaceCard'] = None
    associated_time_period: Optional['TimePeriodCard'] = None
    emotion: Optional[str] = None
    intensity: Optional[int] = None
    
    def __init__(self,
                 title: str,
                 description: str,
                 date: datetime,
                 emotion: Optional[str] = None,
                 intensity: Optional[int] = None,
                 associated_event: Optional[int] = None,
                 associated_people: Optional[List[int]] = None,
                 associated_place: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 id: Optional[int] = None):
        super().__init__(title, description, created_at, updated_at, id)
        self.date = date
        self.emotion = emotion
        self.intensity = intensity
        self.associated_event = associated_event
        self.associated_people = associated_people or []
        self.associated_place = associated_place
    
    def set_event(self, event: 'EventCard') -> None:
        """Set the associated event."""
        self.associated_event = event
    
    def add_person(self, person: 'PersonCard') -> None:
        """Add a person to the memory."""
        if person not in self.associated_people:
            self.associated_people.append(person)
    
    def set_place(self, place: 'PlaceCard') -> None:
        """Set the associated place."""
        self.associated_place = place
    
    def set_time_period(self, time_period: 'TimePeriodCard') -> None:
        """Set the associated time period."""
        self.associated_time_period = time_period
    
    def set_emotion(self, emotion: str, intensity: int) -> None:
        """Set the emotion and its intensity."""
        self.emotion = emotion
        self.intensity = max(0, min(10, intensity))  # Ensure intensity is between 0 and 10
    
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
        
        # Create base card first
        memory = cls(
            title=data['title'],
            description=data['description'],
            date=datetime.fromisoformat(data['date']) if 'date' in data else datetime.now()
        )
        
        # Set base card attributes
        memory.id = data.get('id')
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