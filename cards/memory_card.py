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
    emotion: Optional[str] = None
    intensity: Optional[int] = None
    associated_event: Optional[EventCard] = None
    associated_people: List[PersonCard] = field(default_factory=list)
    associated_place: Optional[PlaceCard] = None
    associated_time_period: Optional[TimePeriodCard] = None
    
    def __post_init__(self):
        """Initialize memory-specific fields after base initialization."""
        super().__post_init__()
        
        # Initialize lists if None
        if self.people is None:
            self.people = []
        if self.emotions is None:
            self.emotions = []
        if self.media_ids is None:
            self.media_ids = []
        if self.associated_people is None:
            self.associated_people = []
            
        # Validate intensity if set
        if self.intensity is not None:
            if not isinstance(self.intensity, int):
                raise ValueError("Intensity must be an integer")
            if not 0 <= self.intensity <= 10:
                raise ValueError("Intensity must be between 0 and 10")
    
    def set_event(self, event: EventCard) -> None:
        """Set the associated event."""
        if not isinstance(event, EventCard):
            raise TypeError("event must be an instance of EventCard")
        self.associated_event = event
        self.updated_at = datetime.now()
    
    def add_person(self, person: PersonCard) -> None:
        """Add a person to the memory."""
        if not isinstance(person, PersonCard):
            raise TypeError("person must be an instance of PersonCard")
        if person not in self.associated_people:
            self.associated_people.append(person)
            self.updated_at = datetime.now()
    
    def set_place(self, place: PlaceCard) -> None:
        """Set the associated place."""
        if not isinstance(place, PlaceCard):
            raise TypeError("place must be an instance of PlaceCard")
        self.associated_place = place
        self.updated_at = datetime.now()
    
    def set_time_period(self, time_period: TimePeriodCard) -> None:
        """Set the associated time period."""
        if not isinstance(time_period, TimePeriodCard):
            raise TypeError("time_period must be an instance of TimePeriodCard")
        self.associated_time_period = time_period
        self.updated_at = datetime.now()
    
    def set_emotion(self, emotion: str, intensity: int) -> None:
        """Set the emotion and its intensity."""
        if not emotion or not emotion.strip():
            raise ValueError("Emotion cannot be empty")
        if not isinstance(intensity, int):
            raise ValueError("Intensity must be an integer")
        if not 0 <= intensity <= 10:
            raise ValueError("Intensity must be between 0 and 10")
            
        self.emotion = emotion.strip()
        self.intensity = intensity
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the memory to a dictionary."""
        data = super().to_dict()
        data.update({
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'people': self.people,
            'emotions': self.emotions,
            'created_by': self.created_by,
            'media_ids': self.media_ids,
            'emotion': self.emotion,
            'intensity': self.intensity,
            'associated_event': self.associated_event.to_dict() if self.associated_event else None,
            'associated_people': [p.to_dict() for p in self.associated_people],
            'associated_place': self.associated_place.to_dict() if self.associated_place else None,
            'associated_time_period': self.associated_time_period.to_dict() if self.associated_time_period else None
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryCard':
        """Create a memory from a dictionary."""
        # Create memory card with base fields
        memory = super().from_dict(data)
        
        # Set memory-specific fields
        memory.date = datetime.fromisoformat(data['date']) if data.get('date') else None
        memory.location = data.get('location')
        memory.people = data.get('people', [])
        memory.emotions = data.get('emotions', [])
        memory.created_by = data.get('created_by')
        memory.media_ids = data.get('media_ids', [])
        memory.emotion = data.get('emotion')
        memory.intensity = data.get('intensity')
        
        # Set associated objects
        if data.get('associated_event'):
            memory.associated_event = EventCard.from_dict(data['associated_event'])
        if data.get('associated_people'):
            memory.associated_people = [PersonCard.from_dict(p) for p in data['associated_people']]
        if data.get('associated_place'):
            memory.associated_place = PlaceCard.from_dict(data['associated_place'])
        if data.get('associated_time_period'):
            memory.associated_time_period = TimePeriodCard.from_dict(data['associated_time_period'])
        
        return memory 