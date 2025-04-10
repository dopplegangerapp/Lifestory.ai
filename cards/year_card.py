from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from .time_period_card import TimePeriodCard
from .event_card import EventCard
from .memory_card import MemoryCard

@dataclass
class YearCard(TimePeriodCard):
    year: int = field(default_factory=lambda: datetime.now().year)
    
    def __post_init__(self):
        """Initialize the year's start and end dates"""
        self.start_date = datetime(self.year, 1, 1)
        self.end_date = datetime(self.year, 12, 31, 23, 59, 59)
        super().__post_init__()
    
    def set_year(self, year: int):
        """Set the year"""
        self.year = year
        self.start_date = datetime(year, 1, 1)
        self.end_date = datetime(year, 12, 31, 23, 59, 59)
    
    def to_dict(self):
        """Convert year to dictionary for JSON serialization"""
        data = super().to_dict()
        data.update({
            'year': self.year
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create year from dictionary"""
        year = super().from_dict(data)
        year.year = data.get('year', datetime.now().year)
        return year 