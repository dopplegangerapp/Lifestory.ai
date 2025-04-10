from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_card import BaseCard

class LocationCard(BaseCard):
    """Card representing a location in the DROE Core system."""
    
    def __init__(self,
                 name: str,
                 description: str,
                 latitude: Optional[float] = None,
                 longitude: Optional[float] = None,
                 created_by: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a location card.
        
        Args:
            name (str): Location name
            description (str): Description of the location
            latitude (float, optional): Geographic latitude
            longitude (float, optional): Geographic longitude
            created_by (int, optional): ID of the user who created the location
            created_at (datetime, optional): When the location was created
            updated_at (datetime, optional): When the location was last updated
            metadata (dict, optional): Additional metadata
        """
        super().__init__(name, description, created_at, updated_at, metadata)
        self.latitude = latitude
        self.longitude = longitude
        self.created_by = created_by
        self.event_ids: List[int] = []
        self.memory_ids: List[int] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the location card to a dictionary for storage."""
        base_dict = super().to_dict()
        location_dict = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_by': self.created_by,
            'event_ids': self.event_ids,
            'memory_ids': self.memory_ids
        }
        return {**base_dict, **location_dict}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LocationCard':
        """Create a location card from a dictionary."""
        card = cls(
            name=data['title'],  # Using title as name
            description=data['description'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            created_by=data.get('created_by'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            metadata=data.get('metadata', {})
        )
        
        card.event_ids = data.get('event_ids', [])
        card.memory_ids = data.get('memory_ids', [])
        
        return card
    
    def add_event(self, event_id: int) -> None:
        """Add an event that occurred at this location."""
        if event_id not in self.event_ids:
            self.event_ids.append(event_id)
            self.updated_at = datetime.now()
    
    def remove_event(self, event_id: int) -> None:
        """Remove an event from this location."""
        if event_id in self.event_ids:
            self.event_ids.remove(event_id)
            self.updated_at = datetime.now()
    
    def add_memory(self, memory_id: int) -> None:
        """Add a memory associated with this location."""
        if memory_id not in self.memory_ids:
            self.memory_ids.append(memory_id)
            self.updated_at = datetime.now()
    
    def remove_memory(self, memory_id: int) -> None:
        """Remove a memory from this location."""
        if memory_id in self.memory_ids:
            self.memory_ids.remove(memory_id)
            self.updated_at = datetime.now()
