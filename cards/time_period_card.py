from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from .base_card import BaseCard

@dataclass
class TimePeriodCard(BaseCard):
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    events: List['EventCard'] = field(default_factory=list)
    memories: List['MemoryCard'] = field(default_factory=list)
    
    def set_dates(self, start_date: datetime, end_date: Optional[datetime] = None) -> None:
        """Set the start and end dates of the time period."""
        self.start_date = start_date
        self.end_date = end_date
    
    def add_event(self, event: 'EventCard') -> None:
        """Add an event that occurred during this time period."""
        if event not in self.events:
            self.events.append(event)
    
    def add_memory(self, memory: 'MemoryCard') -> None:
        """Add a memory associated with this time period."""
        if memory not in self.memories:
            self.memories.append(memory)
    
    def to_dict(self) -> dict:
        """Convert the time period to a dictionary."""
        data = super().to_dict()
        data.update({
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'events': [event.to_dict() for event in self.events],
            'memories': [memory.to_dict() for memory in self.memories]
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TimePeriodCard':
        """Create a time period from a dictionary."""
        from .event_card import EventCard
        from .memory_card import MemoryCard
        
        time_period = super().from_dict(data)
        time_period.start_date = datetime.fromisoformat(data['start_date'])
        if data.get('end_date'):
            time_period.end_date = datetime.fromisoformat(data['end_date'])
        
        if data.get('events'):
            time_period.events = [EventCard.from_dict(e) for e in data['events']]
        if data.get('memories'):
            time_period.memories = [MemoryCard.from_dict(m) for m in data['memories']]
        
        return time_period 