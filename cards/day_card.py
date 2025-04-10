from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass, field
from .time_period_card import TimePeriodCard
from .event_card import EventCard
from .memory_card import MemoryCard

@dataclass
class DayCard(TimePeriodCard):
    date: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize the day's start and end times"""
        self.start_date = self.date.replace(hour=0, minute=0, second=0, microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
        super().__post_init__()
    
    def set_date(self, date: datetime):
        """Set the date of the day"""
        self.date = date
        self.start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        self.end_date = self.start_date + timedelta(days=1)
    
    def to_dict(self):
        """Convert day to dictionary for JSON serialization"""
        data = super().to_dict()
        data.update({
            'date': self.date.isoformat()
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create day from dictionary"""
        day = super().from_dict(data)
        day.date = datetime.fromisoformat(data.get('date', datetime.now().isoformat()))
        return day 