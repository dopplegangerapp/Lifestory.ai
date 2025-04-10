import sqlite3
from flask import g

def get_db():
    """Get database connection from the application context."""
    if 'db' not in g:
        g.db = sqlite3.connect('droecore.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error):
    """Close database connection when the application context ends."""
    db = g.pop('db', None)
    if db is not None:
        db.close() 