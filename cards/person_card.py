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
    
    # Required fields for PersonCard
    name: str = field(init=False)  # Will be set from title in post_init
    
    # Optional fields from BaseCard
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    metadata: Optional[dict] = None
    image_path: str = ""
    media: List['Media'] = field(default_factory=list)
    
    # Optional fields for PersonCard
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    created_by: Optional[str] = None
    media_ids: List[str] = field(default_factory=list)
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize the card after dataclass initialization."""
        super().__post_init__()
        self.name = self.title  # Set name from title
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the person card to a dictionary for storage."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'death_date': self.death_date.isoformat() if self.death_date else None,
            'relationships': {k: v for k, v in self.relationships.items()},
            'created_by': self.created_by,
            'media_ids': self.media_ids,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersonCard':
        """Create a person card from a dictionary."""
        from .event_card import EventCard
        from .memory_card import MemoryCard
        
        # Create person card
        person = cls(
            title=data['title'],
            description=data['description'],
            id=data.get('id'),
            birth_date=datetime.fromisoformat(data['birth_date']) if data.get('birth_date') else None,
            death_date=datetime.fromisoformat(data['death_date']) if data.get('death_date') else None,
            relationships={k: v for k, v in data.get('relationships', {}).items()},
            created_by=data.get('created_by'),
            media_ids=data.get('media_ids', [])
        )
        
        # Set base card attributes
        person.created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        person.updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        person.metadata = data.get('metadata', {})
        person.image_path = data.get('image_path', '')
        
        # Set person-specific attributes
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
