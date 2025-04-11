import unittest
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main import app, db
from init_db import init_db

class TestBase(unittest.TestCase):
    """Base test class for DROE Core tests."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.db = SQLAlchemy(self.app)
        
    def test_app_exists(self):
        """Test that the app exists."""
        self.assertFalse(self.app is None)
        
    def test_app_is_testing(self):
        """Test that the app is in testing mode."""
        self.assertTrue(self.app.config['TESTING'])
        
    @pytest.fixture
    def app(self):
        """Get the Flask app."""
        return self.app
        
    @pytest.fixture
    def db(self):
        """Get the database."""
        return self.db

    @pytest.fixture
    def db(self, app):
        with app.app_context():
            db.create_all()
            init_db()
            yield db
            db.session.remove()
            db.drop_all() 