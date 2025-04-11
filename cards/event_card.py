from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard
from .place_card import PlaceCard
from .time_period_card import TimePeriodCard

@dataclass
class EventCard(BaseCard):
    """Card representing an event in the DROE Core system."""
    
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
    
    # Event-specific fields
    date: Optional[datetime] = None
    location: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    media_ids: List[str] = field(default_factory=list)
    
    def __init__(self,
                 title: str,
                 description: str,
                 date: Optional[datetime] = None,
                 location: Optional[str] = None,
                 participants: Optional[List[str]] = None,
                 emotions: Optional[List[str]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 id: Optional[str] = None,
                 created_by: Optional[str] = None,
                 media_ids: Optional[List[str]] = None):
        """
        Initialize an event card.
        
        Args:
            title (str): Event's title
            description (str): Event's description
            date (datetime, optional): When the event occurred
            location (str, optional): Where the event occurred
            participants (List[str], optional): Who participated in the event
            emotions (List[str], optional): Emotions associated with the event
            created_at (datetime, optional): When the card was created
            updated_at (datetime, optional): When the card was last updated
            id (str, optional): ID of the card
            created_by (str, optional): Who created the card
            media_ids (List[str], optional): IDs of associated media
        """
        super().__init__(title=title, description=description, id=id)
        self.date = date
        self.location = location
        self.participants = participants or []
        self.emotions = emotions or []
        self.created_by = created_by
        self.media_ids = media_ids or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        data = super().to_dict()
        data.update({
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'participants': self.participants,
            'emotions': self.emotions,
            'created_by': self.created_by,
            'media_ids': self.media_ids
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventCard':
        """Create an event from a dictionary."""
        from .person_card import PersonCard
        from .place_card import PlaceCard
        from .time_period_card import TimePeriodCard
        
        # Create event card
        event = cls(
            title=data['title'],
            description=data['description'],
            id=data.get('id'),
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            location=data.get('location'),
            participants=data.get('participants', []),
            emotions=data.get('emotions', []),
            created_by=data.get('created_by'),
            media_ids=data.get('media_ids', [])
        )
        
        # Set base card attributes
        event.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        event.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        event.metadata = data.get('metadata', {})
        event.image_path = data.get('image_path', '')
        
        return event
    
    def add_person(self, person: 'PersonCard') -> None:
        """Add a person to the event."""
        if person.id not in self.participants:
            self.participants.append(person.id)
            self.updated_at = datetime.now()
    
    def remove_person(self, person: 'PersonCard') -> None:
        """Remove a person from the event."""
        if person.id in self.participants:
            self.participants.remove(person.id)
            self.updated_at = datetime.now()
    
    def set_location(self, location: 'PlaceCard') -> None:
        """Set the location of the event."""
        self.location = location.id
        self.updated_at = datetime.now()
    
    def add_emotion(self, emotion: str) -> None:
        """Add an emotion to the event."""
        if emotion not in self.emotions:
            self.emotions.append(emotion)
            self.updated_at = datetime.now()
    
    def remove_emotion(self, emotion: str) -> None:
        """Remove an emotion from the event."""
        if emotion in self.emotions:
            self.emotions.remove(emotion)
            self.updated_at = datetime.now()

    def add_media(self, media_id: str) -> None:
        """Add media to the event."""
        if media_id not in self.media_ids:
            self.media_ids.append(media_id)
            self.updated_at = datetime.now()
    
    def remove_media(self, media_id: str) -> None:
        """Remove media from the event."""
        if media_id in self.media_ids:
            self.media_ids.remove(media_id)
            self.updated_at = datetime.now()
