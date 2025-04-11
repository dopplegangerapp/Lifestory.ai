import unittest
import json
import tempfile
import os
from datetime import datetime
from flask import Flask
from flask.testing import FlaskClient

from api import create_app
from storage.storage_manager import StorageManager
from cards.person_card import PersonCard
from cards.event_card import EventCard

class TestAPI(unittest.TestCase):
    """Tests for the API endpoints."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for storage
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['STORAGE_PATH'] = self.temp_dir
        self.client = self.app.test_client()
        
        # Initialize storage manager
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
        
    def test_create_person(self):
        """Test creating a person via API."""
        # Create person data
        person_data = {
            "name": "John Doe",
            "description": "A test person",
            "birth_date": "1990-01-01T00:00:00",
            "relationships": {"friend": ["person2"]}
        }
        
        # Send POST request
        response = self.client.post(
            '/api/persons',
            data=json.dumps(person_data),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        
        # Verify card was created
        person = self.storage_manager.load_card(response_data['id'])
        self.assertIsNotNone(person)
        self.assertEqual(person.name, "John Doe")
        self.assertEqual(person.description, "A test person")
        self.assertEqual(person.birth_date, datetime(1990, 1, 1))
        self.assertEqual(person.relationships, {"friend": ["person2"]})
        
    def test_create_event(self):
        """Test creating an event via API."""
        # Create event data
        event_data = {
            "title": "Birthday Party",
            "description": "A test event",
            "date": "2023-01-01T00:00:00",
            "location": "Test Location",
            "participants": ["person1"],
            "emotions": ["happy", "excited"]
        }
        
        # Send POST request
        response = self.client.post(
            '/api/events',
            data=json.dumps(event_data),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        
        # Verify card was created
        event = self.storage_manager.load_card(response_data['id'])
        self.assertIsNotNone(event)
        self.assertEqual(event.title, "Birthday Party")
        self.assertEqual(event.description, "A test event")
        self.assertEqual(event.date, datetime(2023, 1, 1))
        self.assertEqual(event.location, "Test Location")
        self.assertEqual(event.participants, ["person1"])
        self.assertEqual(event.emotions, ["happy", "excited"])
        
    def test_get_person(self):
        """Test getting a person via API."""
        # Create and save a person
        person = PersonCard(
            name="John Doe",
            description="A test person"
        )
        self.storage_manager.save_card(person)
        
        # Send GET request
        response = self.client.get(f'/api/persons/{person.id}')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['name'], "John Doe")
        self.assertEqual(response_data['description'], "A test person")
        
    def test_get_event(self):
        """Test getting an event via API."""
        # Create and save an event
        event = EventCard(
            title="Birthday Party",
            description="A test event"
        )
        self.storage_manager.save_card(event)
        
        # Send GET request
        response = self.client.get(f'/api/events/{event.id}')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['title'], "Birthday Party")
        self.assertEqual(response_data['description'], "A test event")
        
    def test_update_person(self):
        """Test updating a person via API."""
        # Create and save a person
        person = PersonCard(
            name="John Doe",
            description="A test person"
        )
        self.storage_manager.save_card(person)
        
        # Update person data
        update_data = {
            "name": "Jane Doe",
            "description": "An updated person"
        }
        
        # Send PUT request
        response = self.client.put(
            f'/api/persons/{person.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        
        # Verify card was updated
        updated_person = self.storage_manager.load_card(person.id)
        self.assertEqual(updated_person.name, "Jane Doe")
        self.assertEqual(updated_person.description, "An updated person")
        
    def test_delete_person(self):
        """Test deleting a person via API."""
        # Create and save a person
        person = PersonCard(
            name="John Doe",
            description="A test person"
        )
        self.storage_manager.save_card(person)
        
        # Send DELETE request
        response = self.client.delete(f'/api/persons/{person.id}')
        
        # Verify response
        self.assertEqual(response.status_code, 204)
        
        # Verify card was deleted
        self.assertIsNone(self.storage_manager.load_card(person.id))
        
    def test_list_persons(self):
        """Test listing persons via API."""
        # Create and save multiple persons
        person1 = PersonCard(
            name="John Doe",
            description="A test person"
        )
        person2 = PersonCard(
            name="Jane Doe",
            description="Another test person"
        )
        self.storage_manager.save_card(person1)
        self.storage_manager.save_card(person2)
        
        # Send GET request
        response = self.client.get('/api/persons')
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 2)
        names = [p['name'] for p in response_data]
        self.assertIn("John Doe", names)
        self.assertIn("Jane Doe", names)
        
if __name__ == '__main__':
    unittest.main() 