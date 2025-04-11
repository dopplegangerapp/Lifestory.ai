from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class PlaceCard(BaseCard):
    """Card representing a place in the DROE Core system."""
    
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
    
    # Place-specific fields
    location: str = ""
    coordinates: Optional[Tuple[float, float]] = None
    created_by: Optional[str] = None
    media_ids: List[str] = field(default_factory=list)
    name: str = field(init=False)  # Will be set from title in post_init
    latitude: float = 0.0
    longitude: float = 0.0
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize place-specific fields after base initialization."""
        super().__post_init__()
        
        # Set name from title
        self.name = self.title
        
        # Initialize lists if None
        if self.media_ids is None:
            self.media_ids = []
        if self.events is None:
            self.events = []
        if self.memories is None:
            self.memories = []
            
        # Set coordinates if provided
        if self.coordinates:
            self.latitude, self.longitude = self.coordinates
            
        # Validate coordinates
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
    
    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set the coordinates of the place."""
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number")
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
            
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.coordinates = (self.latitude, self.longitude)
        self.updated_at = datetime.now()
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event that occurred at this place."""
        if not isinstance(event, 'EventCard'):
            raise TypeError("event must be an instance of EventCard")
        if event not in self.events:
            self.events.append(event)
            self.updated_at = datetime.now()
    
    def remove_event(self, event: 'EventCard') -> None:
        """Remove an event from this place."""
        if event in self.events:
            self.events.remove(event)
            self.updated_at = datetime.now()
    
    def add_memory(self, memory: 'MemoryCard') -> None:
        """Add a memory associated with this place."""
        if not isinstance(memory, 'MemoryCard'):
            raise TypeError("memory must be an instance of MemoryCard")
        if memory not in self.memories:
            self.memories.append(memory)
            self.updated_at = datetime.now()
    
    def remove_memory(self, memory: 'MemoryCard') -> None:
        """Remove a memory from this place."""
        if memory in self.memories:
            self.memories.remove(memory)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the place to a dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'location': self.location,
            'coordinates': self.coordinates,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_by': self.created_by,
            'media_ids': self.media_ids,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlaceCard':
        """Create a place from a dictionary."""
        # Create place card with base fields
        place = super().from_dict(data)
        
        # Set place-specific fields
        place.name = data.get('name', data['title'])
        place.location = data.get('location', '')
        place.created_by = data.get('created_by')
        place.media_ids = data.get('media_ids', [])
        
        # Set coordinates
        if data.get('coordinates'):
            place.coordinates = tuple(data['coordinates'])
            place.latitude, place.longitude = place.coordinates
        else:
            place.latitude = data.get('latitude', 0.0)
            place.longitude = data.get('longitude', 0.0)
            place.coordinates = (place.latitude, place.longitude)
        
        # Set associated objects
        if data.get('events'):
            from .event_card import EventCard
            place.events = [EventCard.from_dict(e) for e in data['events']]
        if data.get('memories'):
            from .memory_card import MemoryCard
            place.memories = [MemoryCard.from_dict(m) for m in data['memories']]
        
        return place 