from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class PersonCard(BaseCard):
    """Card representing a person in the DROE Core system."""
    
    relationship: str = ""
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the person card to a dictionary for storage."""
        data = super().to_dict()
        data.update({
            'relationship': self.relationship,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersonCard':
        """Create a person card from a dictionary."""
        from .event_card import EventCard
        from .memory_card import MemoryCard
        
        # Create base card first
        person = cls(
            title=data['title'],
            description=data['description']
        )
        
        # Set base card attributes
        person.id = data.get('id')
        person.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        person.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        person.metadata = data.get('metadata', {})
        person.image_path = data.get('image_path', '')
        
        # Set person-specific attributes
        person.relationship = data.get('relationship', '')
        person.events = [EventCard.from_dict(e) for e in data.get('events', [])]
        person.memories = [MemoryCard.from_dict(m) for m in data.get('memories', [])]
        
        return person
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event to the person's history."""
        if event not in self.events:
            self.events.append(event)
            self.updated_at = datetime.now()
    
    def remove_event(self, event: 'EventCard') -> None:
        """Remove an event from the person's history."""
        if event in self.events:
            self.events.remove(event)
            self.updated_at = datetime.now()
    
    def add_memory(self, memory: 'MemoryCard') -> None:
        """Add a memory about the person."""
        if memory not in self.memories:
            self.memories.append(memory)
            self.updated_at = datetime.now()
    
    def remove_memory(self, memory: 'MemoryCard') -> None:
        """Remove a memory about the person."""
        if memory in self.memories:
            self.memories.remove(memory)
            self.updated_at = datetime.now()
