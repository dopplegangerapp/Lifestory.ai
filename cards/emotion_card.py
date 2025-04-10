from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_card import BaseCard

class EmotionCard(BaseCard):
    """Card representing an emotion in the DROE Core system."""
    
    def __init__(self,
                 name: str,
                 description: str,
                 intensity: Optional[float] = None,
                 created_by: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize an emotion card.
        
        Args:
            name (str): Emotion name
            description (str): Description of the emotion
            intensity (float, optional): Intensity level (0.0 to 1.0)
            created_by (int, optional): ID of the user who created the emotion
            created_at (datetime, optional): When the emotion was created
            updated_at (datetime, optional): When the emotion was last updated
            metadata (dict, optional): Additional metadata
        """
        super().__init__(name, description, created_at, updated_at, metadata)
        self.intensity = intensity
        self.created_by = created_by
        self.event_ids: List[int] = []
        self.memory_ids: List[int] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the emotion card to a dictionary for storage."""
        base_dict = super().to_dict()
        emotion_dict = {
            'intensity': self.intensity,
            'created_by': self.created_by,
            'event_ids': self.event_ids,
            'memory_ids': self.memory_ids
        }
        return {**base_dict, **emotion_dict}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmotionCard':
        """Create an emotion card from a dictionary."""
        card = cls(
            name=data['title'],  # Using title as name
            description=data['description'],
            intensity=data.get('intensity'),
            created_by=data.get('created_by'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            metadata=data.get('metadata', {})
        )
        
        card.event_ids = data.get('event_ids', [])
        card.memory_ids = data.get('memory_ids', [])
        
        return card
    
    def add_event(self, event_id: int) -> None:
        """Add an event associated with this emotion."""
        if event_id not in self.event_ids:
            self.event_ids.append(event_id)
            self.updated_at = datetime.now()
    
    def remove_event(self, event_id: int) -> None:
        """Remove an event from this emotion."""
        if event_id in self.event_ids:
            self.event_ids.remove(event_id)
            self.updated_at = datetime.now()
    
    def add_memory(self, memory_id: int) -> None:
        """Add a memory associated with this emotion."""
        if memory_id not in self.memory_ids:
            self.memory_ids.append(memory_id)
            self.updated_at = datetime.now()
    
    def remove_memory(self, memory_id: int) -> None:
        """Remove a memory from this emotion."""
        if memory_id in self.memory_ids:
            self.memory_ids.remove(memory_id)
            self.updated_at = datetime.now()
