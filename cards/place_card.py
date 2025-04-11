from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class PlaceCard(BaseCard):
    """Card representing a place in the DROE Core system."""
    
    name: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def __init__(self,
                 title: str,
                 description: str,
                 name: str,
                 latitude: float = 0.0,
                 longitude: float = 0.0,
                 events: Optional[List['EventCard']] = None,
                 memories: Optional[List['MemoryCard']] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 id: Optional[str] = None):
        """
        Initialize a place card.
        
        Args:
            title (str): Place's title
            description (str): Place's description
            name (str): Place's name
            latitude (float, optional): Place's latitude
            longitude (float, optional): Place's longitude
            events (List[EventCard], optional): Events at this place
            memories (List[MemoryCard], optional): Memories about this place
            created_at (datetime, optional): When the card was created
            updated_at (datetime, optional): When the card was last updated
            id (str, optional): ID of the card
        """
        super().__init__(title=title, description=description, id=id)
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.events = events or []
        self.memories = memories or []
    
    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set the coordinates of the place."""
        self.latitude = latitude
        self.longitude = longitude
        self.updated_at = datetime.now()
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event that occurred at this place."""
        if event not in self.events:
            self.events.append(event)
            self.updated_at = datetime.now()
    
    def add_memory(self, memory: 'MemoryCard') -> None:
        """Add a memory associated with this place."""
        if memory not in self.memories:
            self.memories.append(memory)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the place to a dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlaceCard':
        """Create a place from a dictionary."""
        from .event_card import EventCard
        from .memory_card import MemoryCard
        
        # Create base card first
        place = cls(
            title=data['title'],
            description=data['description'],
            name=data.get('name', ''),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0)
        )
        
        # Set base card attributes
        place.id = data.get('id')
        place.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        place.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        place.metadata = data.get('metadata', {})
        place.image_path = data.get('image_path', '')
        
        # Set place-specific attributes
        place.events = [EventCard.from_dict(e) for e in data.get('events', [])]
        place.memories = [MemoryCard.from_dict(m) for m in data.get('memories', [])]
        
        return place 