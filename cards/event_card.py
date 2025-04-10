from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard
from .place_card import PlaceCard
from .time_period_card import TimePeriodCard

@dataclass
class EventCard(BaseCard):
    """Card representing an event in the DROE Core system."""
    
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    people: List['PersonCard'] = field(default_factory=list)
    location: Optional['PlaceCard'] = None
    time_period: Optional['TimePeriodCard'] = None
    location_id: Optional[int] = None
    created_by: Optional[int] = None
    people_ids: List[int] = field(default_factory=list)
    media_ids: List[int] = field(default_factory=list)
    
    def __init__(self,
                 title: str,
                 description: str,
                 start_date: datetime,
                 end_date: Optional[datetime] = None,
                 location: Optional['PlaceCard'] = None,
                 people: Optional[List['PersonCard']] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 id: Optional[int] = None):
        """
        Initialize an event card.
        
        Args:
            title (str): Event title
            description (str): Event description
            start_date (datetime): When the event starts
            end_date (datetime, optional): When the event ends
            location (PlaceCard, optional): The location of the event
            people (List[PersonCard], optional): People attending the event
            created_at (datetime, optional): When the event was created
            updated_at (datetime, optional): When the event was last updated
            id (int, optional): ID of the event
        """
        super().__init__(title, description, created_at, updated_at, id)
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.people = people or []
        self.location_id = location.id if location else None
        self.created_by = None
        self.people_ids = [person.id for person in people] if people else []
        self.media_ids = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        data = super().to_dict()
        data.update({
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'people': [p.to_dict() for p in self.people],
            'location': self.location.to_dict() if self.location else None,
            'time_period': self.time_period.to_dict() if self.time_period else None
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventCard':
        """Create an event from a dictionary."""
        from .person_card import PersonCard
        from .place_card import PlaceCard
        from .time_period_card import TimePeriodCard
        
        # Create base card first
        event = cls(
            title=data['title'],
            description=data['description'],
            start_date=datetime.fromisoformat(data['start_date']) if 'start_date' in data else datetime.now()
        )
        
        # Set base card attributes
        event.id = data.get('id')
        event.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        event.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        event.metadata = data.get('metadata', {})
        event.image_path = data.get('image_path', '')
        
        # Set event-specific attributes
        event.end_date = datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
        event.people = [PersonCard.from_dict(p) for p in data.get('people', [])]
        event.location = PlaceCard.from_dict(data['location']) if data.get('location') else None
        event.time_period = TimePeriodCard.from_dict(data['time_period']) if data.get('time_period') else None
        
        return event
    
    def add_person(self, person: 'PersonCard') -> None:
        """Add a person to the event."""
        if person not in self.people:
            self.people.append(person)

    def set_location(self, place: 'PlaceCard') -> None:
        """Set the location of the event."""
        self.location = place

    def set_time_period(self, time_period: 'TimePeriodCard') -> None:
        """Set the time period of the event."""
        self.time_period = time_period

    def add_media(self, media_id: int) -> None:
        """Add media to the event."""
        if media_id not in self.media_ids:
            self.media_ids.append(media_id)
            self.updated_at = datetime.now()
    
    def remove_media(self, media_id: int) -> None:
        """Remove media from the event."""
        if media_id in self.media_ids:
            self.media_ids.remove(media_id)
            self.updated_at = datetime.now()
