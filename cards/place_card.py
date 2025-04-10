from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class PlaceCard(BaseCard):
    latitude: float = 0.0
    longitude: float = 0.0
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set the coordinates of the place."""
        self.latitude = latitude
        self.longitude = longitude
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event that occurred at this place."""
        if event not in self.events:
            self.events.append(event)
    
    def add_memory(self, memory: 'MemoryCard') -> None:
        """Add a memory associated with this place."""
        if memory not in self.memories:
            self.memories.append(memory)
    
    def to_dict(self) -> dict:
        """Convert the place to a dictionary."""
        data = super().to_dict()
        data.update({
            'latitude': self.latitude,
            'longitude': self.longitude,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlaceCard':
        """Create a place from a dictionary."""
        from .event_card import EventCard
        from .memory_card import MemoryCard
        
        place = super().from_dict(data)
        place.latitude = data.get('latitude', 0.0)
        place.longitude = data.get('longitude', 0.0)
        
        if data.get('events'):
            place.events = [EventCard.from_dict(e) for e in data['events']]
        if data.get('memories'):
            place.memories = [MemoryCard.from_dict(m) for m in data['memories']]
        
        return place 