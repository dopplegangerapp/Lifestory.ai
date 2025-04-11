from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from utils.image_generator import ImageGenerator
from .media import Media
import uuid

@dataclass
class BaseCard:
    """Base class for all card types in the DROE Core system."""
    
    title: str
    description: str
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    metadata: Optional[dict] = None
    image_path: str = ""
    media: List[Media] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize any fields that need post-initialization setup."""
        # Validate required fields
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if not self.description or not self.description.strip():
            raise ValueError("Description is required")
            
        # Clean up fields
        self.title = self.title.strip()
        self.description = self.description.strip()
        
        # Set default values
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.image_path:
            self.generate_default_image()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}
        if self.media is None:
            self.media = []
    
    def generate_default_image(self):
        """Generate a default image for the card using DALL-E"""
        try:
            image_generator = ImageGenerator()
            prompt = f"Create an abstract image representing {self.title}"
            image_url = image_generator.generate_image(prompt)
            if image_url:
                self.image_path = image_url
        except Exception as e:
            print(f"Error generating default image: {str(e)}")
            self.image_path = "/static/images/default_card.png"
    
    def add_media(self, media: Media) -> None:
        """Add media to the card."""
        if not isinstance(media, Media):
            raise TypeError("media must be an instance of Media")
        if media not in self.media:
            self.media.append(media)
            self.updated_at = datetime.now()
    
    def remove_media(self, media: Media) -> None:
        """Remove media from the card."""
        if media in self.media:
            self.media.remove(media)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the card to a dictionary."""
        if self.created_at is None:
            self.created_at = datetime.now()
            
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'metadata': self.metadata,
            'image_path': self.image_path,
            'media': [m.to_dict() for m in self.media]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseCard':
        """Create a card from a dictionary."""
        # Validate required fields
        if not data.get('title'):
            raise ValueError("Title is required")
        if not data.get('description'):
            raise ValueError("Description is required")
            
        media_list = [Media.from_dict(m) for m in data.get('media', [])]
        created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        updated_at = datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else None
        
        return cls(
            title=data['title'],
            description=data['description'],
            id=data.get('id'),
            created_at=created_at,
            updated_at=updated_at,
            metadata=data.get('metadata', {}),
            image_path=data.get('image_path', ''),
            media=media_list
        )
    
    def update(self, **kwargs) -> None:
        """Update card properties."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key in ['title', 'description'] and not value:
                    raise ValueError(f"{key.capitalize()} cannot be empty")
                setattr(self, key, value.strip() if isinstance(value, str) else value)
        self.updated_at = datetime.now()
