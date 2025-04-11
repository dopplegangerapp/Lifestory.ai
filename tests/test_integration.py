import unittest
import os
import json
import tempfile
from datetime import datetime
from typing import Dict, Any

from cards.base_card import BaseCard
from cards.person_card import PersonCard
from cards.event_card import EventCard
from cards.place_card import PlaceCard
from cards.memory_card import MemoryCard
from cards.time_period_card import TimePeriodCard
from storage.storage_manager import StorageManager

class TestIntegration(unittest.TestCase):
    """Integration tests for the DROE Core system."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for storage
        self.temp_dir = tempfile.mkdtemp()
        self.storage_manager = StorageManager(self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)
        
    def test_person_card_creation(self):
        """Test creating and saving a person card."""
        # Create person card
        person = PersonCard(
            name="John Doe",
            description="A test person",
            birth_date=datetime(1990, 1, 1),
            relationships={"friend": ["person2"]}
        )
        
        # Save card
        self.storage_manager.save_card(person)
        
        # Load card
        loaded_person = self.storage_manager.load_card(person.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_person)
        self.assertEqual(loaded_person.name, "John Doe")
        self.assertEqual(loaded_person.description, "A test person")
        self.assertEqual(loaded_person.birth_date, datetime(1990, 1, 1))
        self.assertEqual(loaded_person.relationships, {"friend": ["person2"]})
        
    def test_event_card_creation(self):
        """Test creating and saving an event card."""
        # Create event card
        event = EventCard(
            title="Birthday Party",
            description="A test event",
            date=datetime(2023, 1, 1),
            location="Test Location",
            participants=["person1"],
            emotions=["happy", "excited"]
        )
        
        # Save card
        self.storage_manager.save_card(event)
        
        # Load card
        loaded_event = self.storage_manager.load_card(event.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_event)
        self.assertEqual(loaded_event.title, "Birthday Party")
        self.assertEqual(loaded_event.description, "A test event")
        self.assertEqual(loaded_event.date, datetime(2023, 1, 1))
        self.assertEqual(loaded_event.location, "Test Location")
        self.assertEqual(loaded_event.participants, ["person1"])
        self.assertEqual(loaded_event.emotions, ["happy", "excited"])
        
    def test_place_card_creation(self):
        """Test creating and saving a place card."""
        # Create place card
        place = PlaceCard(
            title="Test Place",
            description="A test place",
            location="Test Location",
            coordinates={"lat": 0.0, "lng": 0.0}
        )
        
        # Save card
        self.storage_manager.save_card(place)
        
        # Load card
        loaded_place = self.storage_manager.load_card(place.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_place)
        self.assertEqual(loaded_place.title, "Test Place")
        self.assertEqual(loaded_place.description, "A test place")
        self.assertEqual(loaded_place.location, "Test Location")
        self.assertEqual(loaded_place.coordinates, {"lat": 0.0, "lng": 0.0})
        
    def test_memory_card_creation(self):
        """Test creating and saving a memory card."""
        # Create memory card
        memory = MemoryCard(
            title="Test Memory",
            description="A test memory",
            date=datetime(2023, 1, 1),
            emotions=["happy"],
            associated_people=["person1"]
        )
        
        # Save card
        self.storage_manager.save_card(memory)
        
        # Load card
        loaded_memory = self.storage_manager.load_card(memory.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_memory)
        self.assertEqual(loaded_memory.title, "Test Memory")
        self.assertEqual(loaded_memory.description, "A test memory")
        self.assertEqual(loaded_memory.date, datetime(2023, 1, 1))
        self.assertEqual(loaded_memory.emotions, ["happy"])
        self.assertEqual(loaded_memory.associated_people, ["person1"])
        
    def test_time_period_card_creation(self):
        """Test creating and saving a time period card."""
        # Create time period card
        time_period = TimePeriodCard(
            title="Test Period",
            description="A test time period",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2023, 1, 1),
            events=["event1"]
        )
        
        # Save card
        self.storage_manager.save_card(time_period)
        
        # Load card
        loaded_time_period = self.storage_manager.load_card(time_period.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_time_period)
        self.assertEqual(loaded_time_period.title, "Test Period")
        self.assertEqual(loaded_time_period.description, "A test time period")
        self.assertEqual(loaded_time_period.start_date, datetime(2020, 1, 1))
        self.assertEqual(loaded_time_period.end_date, datetime(2023, 1, 1))
        self.assertEqual(loaded_time_period.events, ["event1"])
        
    def test_card_deletion(self):
        """Test deleting a card."""
        # Create and save a card
        person = PersonCard(
            name="John Doe",
            description="A test person"
        )
        self.storage_manager.save_card(person)
        
        # Delete card
        self.assertTrue(self.storage_manager.delete_card(person.id))
        
        # Verify card is deleted
        self.assertIsNone(self.storage_manager.load_card(person.id))
        
    def test_card_listing(self):
        """Test listing all cards."""
        # Create and save multiple cards
        person = PersonCard(
            name="John Doe",
            description="A test person"
        )
        event = EventCard(
            title="Birthday Party",
            description="A test event"
        )
        
        self.storage_manager.save_card(person)
        self.storage_manager.save_card(event)
        
        # List cards
        card_ids = self.storage_manager.list_cards()
        
        # Verify card IDs
        self.assertEqual(len(card_ids), 2)
        self.assertIn(person.id, card_ids)
        self.assertIn(event.id, card_ids)
        
    def test_card_type_registration(self):
        """Test registering a new card type."""
        # Create a custom card class
        class CustomCard(BaseCard):
            def __init__(self, title: str, description: str, custom_field: str):
                super().__init__(title=title, description=description)
                self.custom_field = custom_field
                
            def to_dict(self) -> Dict[str, Any]:
                data = super().to_dict()
                data['custom_field'] = self.custom_field
                return data
                
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> 'CustomCard':
                return cls(
                    title=data['title'],
                    description=data['description'],
                    custom_field=data['custom_field']
                )
                
        # Register custom card type
        self.storage_manager.register_card_type('custom', CustomCard)
        
        # Create and save custom card
        custom = CustomCard(
            title="Custom Card",
            description="A test custom card",
            custom_field="test"
        )
        self.storage_manager.save_card(custom)
        
        # Load card
        loaded_custom = self.storage_manager.load_card(custom.id)
        
        # Verify loaded card
        self.assertIsNotNone(loaded_custom)
        self.assertEqual(loaded_custom.title, "Custom Card")
        self.assertEqual(loaded_custom.description, "A test custom card")
        self.assertEqual(loaded_custom.custom_field, "test")
        
if __name__ == '__main__':
    unittest.main() 