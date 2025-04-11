from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class PersonCard(BaseCard):
    """Card representing a person in the DROE Core system."""
    
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
    
    # Person-specific fields
    name: str = ""
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    relationships: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    media_ids: List[str] = field(default_factory=list)
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize person-specific fields after base initialization."""
        super().__post_init__()
        
        # Set name from title if not provided
        if not self.name:
            self.name = self.title
            
        # Initialize lists if None
        if self.relationships is None:
            self.relationships = []
        if self.media_ids is None:
            self.media_ids = []
        if self.events is None:
            self.events = []
        if self.memories is None:
            self.memories = []
            
        # Validate dates if set
        if self.birth_date and self.death_date:
            if self.birth_date > self.death_date:
                raise ValueError("Birth date cannot be after death date")
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event to the person's history."""
        if not isinstance(event, 'EventCard'):
            raise TypeError("event must be an instance of EventCard")
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
        if not isinstance(memory, 'MemoryCard'):
            raise TypeError("memory must be an instance of MemoryCard")
        if memory not in self.memories:
            self.memories.append(memory)
            self.updated_at = datetime.now()
    
    def remove_memory(self, memory: 'MemoryCard') -> None:
        """Remove a memory about the person."""
        if memory in self.memories:
            self.memories.remove(memory)
            self.updated_at = datetime.now()
    
    def add_relationship(self, relationship: str) -> None:
        """Add a relationship to the person."""
        if not relationship or not relationship.strip():
            raise ValueError("Relationship cannot be empty")
        relationship = relationship.strip()
        if relationship not in self.relationships:
            self.relationships.append(relationship)
            self.updated_at = datetime.now()
    
    def remove_relationship(self, relationship: str) -> None:
        """Remove a relationship from the person."""
        if relationship in self.relationships:
            self.relationships.remove(relationship)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the person card to a dictionary for storage."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'death_date': self.death_date.isoformat() if self.death_date else None,
            'relationships': self.relationships,
            'created_by': self.created_by,
            'media_ids': self.media_ids,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersonCard':
        """Create a person card from a dictionary."""
        # Create person card with base fields
        person = super().from_dict(data)
        
        # Set person-specific fields
        person.name = data.get('name', data['title'])
        if data.get('birth_date'):
            person.birth_date = datetime.fromisoformat(data['birth_date'])
        if data.get('death_date'):
            person.death_date = datetime.fromisoformat(data['death_date'])
        person.relationships = data.get('relationships', [])
        person.created_by = data.get('created_by')
        person.media_ids = data.get('media_ids', [])
        
        # Set associated objects
        if data.get('events'):
            from .event_card import EventCard
            person.events = [EventCard.from_dict(e) for e in data['events']]
        if data.get('memories'):
            from .memory_card import MemoryCard
            person.memories = [MemoryCard.from_dict(m) for m in data['memories']]
        
        return person
