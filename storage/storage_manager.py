from typing import Dict, Any, List, Optional, Type
from datetime import datetime
import json
import os
from cards.base_card import BaseCard
from cards.event_card import EventCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from cards.memory_card import MemoryCard
from cards.time_period_card import TimePeriodCard
from utils.logger import get_logger

class StorageManager:
    """Manages storage of cards in the DROE Core system."""
    
    def __init__(self, storage_path: str):
        """
        Initialize the storage manager.
        
        Args:
            storage_path (str): Path to the storage directory
        """
        self.storage_path = storage_path
        self.logger = get_logger(__name__)
        self.card_types = {
            'event': EventCard,
            'person': PersonCard,
            'place': PlaceCard,
            'memory': MemoryCard,
            'time_period': TimePeriodCard
        }
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        for card_type in self.card_types.keys():
            os.makedirs(os.path.join(storage_path, card_type), exist_ok=True)
        
    def _get_card_path(self, card_id: str, card_type: str) -> str:
        """Get the path to a card's storage file."""
        return os.path.join(self.storage_path, card_type, f"{card_id}.json")
        
    def save_card(self, card: BaseCard) -> None:
        """
        Save a card to storage.
        
        Args:
            card (BaseCard): The card to save
        """
        card_type = card.__class__.__name__.lower().replace('card', '')
        if card_type not in self.card_types:
            raise ValueError(f"Unsupported card type: {card.__class__}")
            
        card_path = self._get_card_path(card.id, card_type)
        card_data = card.to_dict()
        
        # Add card type information
        card_data['type'] = card_type
        
        with open(card_path, 'w') as f:
            json.dump(card_data, f, indent=2)
            
    def load_card(self, card_id: str, card_type: str) -> Optional[BaseCard]:
        """
        Load a card from storage.
        
        Args:
            card_id (str): The ID of the card to load
            card_type (str): The type of the card
            
        Returns:
            Optional[BaseCard]: The loaded card, or None if not found
        """
        if card_type not in self.card_types:
            raise ValueError(f"Unsupported card type: {card_type}")
            
        card_path = self._get_card_path(card_id, card_type)
        
        if not os.path.exists(card_path):
            self.logger.warning(f"Card {card_id} not found in storage")
            return None
            
        with open(card_path, 'r') as f:
            card_data = json.load(f)
            
        # Get card class
        card_class = self.card_types[card_type]
        
        # Create card instance
        return card_class.from_dict(card_data)
        
    def delete_card(self, card_id: str, card_type: str) -> bool:
        """
        Delete a card from storage.
        
        Args:
            card_id (str): The ID of the card to delete
            card_type (str): The type of the card
            
        Returns:
            bool: True if the card was deleted, False otherwise
        """
        if card_type not in self.card_types:
            raise ValueError(f"Unsupported card type: {card_type}")
            
        card_path = self._get_card_path(card_id, card_type)
        
        if not os.path.exists(card_path):
            self.logger.warning(f"Card {card_id} not found in storage")
            return False
            
        os.remove(card_path)
        return True
        
    def list_cards(self, card_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all cards of a specific type.
        
        Args:
            card_type (Optional[str]): The type of cards to list
            
        Returns:
            List[Dict[str, Any]]: List of card metadata
        """
        cards = []
        types_to_list = [card_type] if card_type else self.card_types.keys()
        
        for ctype in types_to_list:
            if ctype not in self.card_types:
                continue
                
            type_path = os.path.join(self.storage_path, ctype)
            if not os.path.exists(type_path):
                continue
                
            for filename in os.listdir(type_path):
                if not filename.endswith('.json'):
                    continue
                    
                with open(os.path.join(type_path, filename), 'r') as f:
                    try:
                        data = json.load(f)
                        cards.append({
                            'id': data.get('id'),
                            'title': data.get('title'),
                            'description': data.get('description'),
                            'type': ctype,
                            'created_at': data.get('created_at'),
                            'updated_at': data.get('updated_at')
                        })
                    except Exception as e:
                        self.logger.error(f"Error loading card {filename}: {str(e)}")
                        continue
                        
        return cards
        
    def get_card_type(self, card: BaseCard) -> str:
        """
        Get the type of a card.
        
        Args:
            card (BaseCard): The card to get the type of
            
        Returns:
            str: The card type
        """
        return card.__class__.__name__.lower()
        
    def register_card_type(self, card_type: str, card_class: Type[BaseCard]) -> None:
        """
        Register a new card type.
        
        Args:
            card_type (str): The type name
            card_class (Type[BaseCard]): The card class
        """
        self.card_types[card_type] = card_class 