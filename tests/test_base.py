import unittest
import os
import tempfile
from main import app, db
from init_db import init_db

class TestBase(unittest.TestCase):
    def setUp(self):
        # Configure test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        # Initialize the database
        with app.app_context():
            db.create_all()
            init_db()
    
    def tearDown(self):
        # Clean up database
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_app_exists(self):
        self.assertFalse(app is None)
    
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING']) 