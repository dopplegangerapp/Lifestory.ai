from tests.test_base import TestBase
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from datetime import datetime

class TestCards(TestBase):
    def test_event_card_creation(self):
        event = EventCard(
            title="Test Event",
            description="Test Description",
            start_date=datetime.now()
        )
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.description, "Test Description")
        self.assertIsNotNone(event.start_date)
    
    def test_memory_card_creation(self):
        memory = MemoryCard(
            title="Test Memory",
            description="Test Description",
            date=datetime.now()
        )
        self.assertEqual(memory.title, "Test Memory")
        self.assertEqual(memory.description, "Test Description")
        self.assertIsNotNone(memory.date)
    
    def test_person_card_creation(self):
        person = PersonCard(
            title="Test Person",
            description="Test Description",
            relationship="Friend"
        )
        self.assertEqual(person.title, "Test Person")
        self.assertEqual(person.description, "Test Description")
        self.assertEqual(person.relationship, "Friend")
    
    def test_event_card_to_dict(self):
        now = datetime.now()
        event = EventCard(
            title="Test Event",
            description="Test Description",
            start_date=now,
            created_at=now
        )
        event_dict = event.to_dict()
        self.assertEqual(event_dict['title'], "Test Event")
        self.assertEqual(event_dict['description'], "Test Description")
        self.assertIn('start_date', event_dict)
    
    def test_memory_card_to_dict(self):
        now = datetime.now()
        memory = MemoryCard(
            title="Test Memory",
            description="Test Description",
            date=now,
            created_at=now
        )
        memory_dict = memory.to_dict()
        self.assertEqual(memory_dict['title'], "Test Memory")
        self.assertEqual(memory_dict['description'], "Test Description")
        self.assertIn('date', memory_dict)
    
    def test_person_card_to_dict(self):
        now = datetime.now()
        person = PersonCard(
            title="Test Person",
            description="Test Description",
            relationship="Friend",
            created_at=now
        )
        person_dict = person.to_dict()
        self.assertEqual(person_dict['title'], "Test Person")
        self.assertEqual(person_dict['description'], "Test Description")
        self.assertEqual(person_dict['relationship'], "Friend")
    
    def test_event_card_from_dict(self):
        now = datetime.now()
        event_data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'start_date': now.isoformat(),
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        event = EventCard.from_dict(event_data)
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.description, "Test Description")
        self.assertIsNotNone(event.start_date)
    
    def test_memory_card_from_dict(self):
        now = datetime.now()
        memory_data = {
            'title': 'Test Memory',
            'description': 'Test Description',
            'date': now.isoformat(),
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        memory = MemoryCard.from_dict(memory_data)
        self.assertEqual(memory.title, "Test Memory")
        self.assertEqual(memory.description, "Test Description")
        self.assertIsNotNone(memory.date)
    
    def test_person_card_from_dict(self):
        now = datetime.now()
        person_data = {
            'title': 'Test Person',
            'description': 'Test Description',
            'relationship': 'Friend',
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        person = PersonCard.from_dict(person_data)
        self.assertEqual(person.title, "Test Person")
        self.assertEqual(person.description, "Test Description")
        self.assertEqual(person.relationship, "Friend") 