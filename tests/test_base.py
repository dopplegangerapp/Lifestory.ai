import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main import app, db
from init_db import init_db

class TestBase:
    @pytest.fixture
    def app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    @pytest.fixture
    def db(self, app):
        with app.app_context():
            db.create_all()
            init_db()
            yield db
            db.session.remove()
            db.drop_all()

    def test_app_exists(self):
        self.assertFalse(app is None)
    
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING']) 