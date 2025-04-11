from typing import Dict, Any, List, Optional
from datetime import datetime
from cards.base_card import BaseCard
from cards.event_card import EventCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from cards.memory_card import MemoryCard
from cards.time_period_card import TimePeriodCard
from storage.storage_manager import StorageManager
from utils.logger import get_logger

logger = get_logger(__name__)

class DROECore:
    """Main system class for managing life stories."""
    
    def __init__(self, storage_path: str = "data"):
        """
        Initialize the DROE Core system.
        
        Args:
            storage_path (str): Path to the storage directory
        """
        self.storage_manager = StorageManager(storage_path)
        self._card_types = {
            'event': EventCard,
            'person': PersonCard,
            'place': PlaceCard,
            'memory': MemoryCard,
            'time_period': TimePeriodCard
        }
    
    def save_card(self, card: BaseCard) -> None:
        """
        Save a card to storage.
        
        Args:
            card (BaseCard): The card to save
        """
        try:
            self.storage_manager.save_card(card)
            logger.info(f"Saved card: {card.title}")
        except Exception as e:
            logger.error(f"Error saving card: {str(e)}")
            raise
    
    def load_card(self, card_id: str, card_type: str) -> Optional[BaseCard]:
        """
        Load a card from storage.
        
        Args:
            card_id (str): The ID of the card to load
            card_type (str): The type of the card
            
        Returns:
            Optional[BaseCard]: The loaded card, or None if not found
        """
        try:
            return self.storage_manager.load_card(card_id, card_type)
        except Exception as e:
            logger.error(f"Error loading card: {str(e)}")
            return None
    
    def delete_card(self, card_id: str, card_type: str) -> bool:
        """
        Delete a card from storage.
        
        Args:
            card_id (str): The ID of the card to delete
            card_type (str): The type of the card
            
        Returns:
            bool: True if the card was deleted, False otherwise
        """
        try:
            return self.storage_manager.delete_card(card_id, card_type)
        except Exception as e:
            logger.error(f"Error deleting card: {str(e)}")
            return False
    
    def list_cards(self, card_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all cards of a specific type.
        
        Args:
            card_type (Optional[str]): The type of cards to list
            
        Returns:
            List[Dict[str, Any]]: List of card metadata
        """
        try:
            return self.storage_manager.list_cards(card_type)
        except Exception as e:
            logger.error(f"Error listing cards: {str(e)}")
            return []
    
    def search_cards(self, query: str, card_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for cards matching a query.
        
        Args:
            query (str): The search query
            card_type (Optional[str]): The type of cards to search
            
        Returns:
            List[Dict[str, Any]]: List of matching card metadata
        """
        try:
            return self.storage_manager.search_cards(query, card_type)
        except Exception as e:
            logger.error(f"Error searching cards: {str(e)}")
            return []
    
    def create_event(self, title: str, description: str, location: Optional[str] = None,
                    participants: Optional[List[str]] = None) -> EventCard:
        """
        Create a new event card.
        
        Args:
            title (str): Event's title
            description (str): Event's description
            location (Optional[str]): Where the event occurred
            participants (Optional[List[str]]): People involved in the event
            
        Returns:
            EventCard: The created event card
        """
        event = EventCard(
            title=title,
            description=description,
            location=location,
            participants=participants or []
        )
        self.save_card(event)
        return event
    
    def create_person(self, title: str, description: str, name: str) -> PersonCard:
        """
        Create a new person card.
        
        Args:
            title (str): Person's title
            description (str): Person's description
            name (str): Person's name
            
        Returns:
            PersonCard: The created person card
        """
        person = PersonCard(
            name=name,
            title=title,
            description=description
        )
        self.save_card(person)
        return person
    
    def create_place(self, title: str, description: str, name: str,
                    latitude: float = 0.0, longitude: float = 0.0) -> PlaceCard:
        """
        Create a new place card.
        
        Args:
            title (str): Place's title
            description (str): Place's description
            name (str): Place's name
            latitude (float): Place's latitude
            longitude (float): Place's longitude
            
        Returns:
            PlaceCard: The created place card
        """
        place = PlaceCard(
            title=title,
            description=description,
            name=name,
            latitude=latitude,
            longitude=longitude
        )
        self.save_card(place)
        return place
    
    def create_memory(self, title: str, description: str) -> MemoryCard:
        """
        Create a new memory card.
        
        Args:
            title (str): Memory's title
            description (str): Memory's description
            
        Returns:
            MemoryCard: The created memory card
        """
        memory = MemoryCard(
            title=title,
            description=description
        )
        self.save_card(memory)
        return memory 