from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

@dataclass
class Media:
    id: Optional[int] = None
    file_path: str = ""
    type: MediaType = MediaType.IMAGE
    created_at: datetime = field(default_factory=datetime.now)
    description: str = ""
    
    def to_dict(self):
        """Convert media to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'file_path': self.file_path,
            'type': self.type.value,
            'created_at': self.created_at.isoformat(),
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create media from dictionary"""
        return cls(
            id=data.get('id'),
            file_path=data.get('file_path', ''),
            type=MediaType(data.get('type', MediaType.IMAGE.value)),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            description=data.get('description', '')
        ) 