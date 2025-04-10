import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect('droecore.db')
    cursor = conn.cursor()
    
    # Create base cards table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP,
        metadata TEXT,
        image_path TEXT
    )
    ''')
    
    # Create events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        location_id INTEGER,
        created_by INTEGER,
        FOREIGN KEY (id) REFERENCES cards(id),
        FOREIGN KEY (location_id) REFERENCES places(id)
    )
    ''')
    
    # Create memories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY,
        date TIMESTAMP,
        emotion TEXT,
        intensity INTEGER,
        event_id INTEGER,
        place_id INTEGER,
        time_period_id INTEGER,
        FOREIGN KEY (id) REFERENCES cards(id),
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (place_id) REFERENCES places(id),
        FOREIGN KEY (time_period_id) REFERENCES time_periods(id)
    )
    ''')
    
    # Create people table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        relationship TEXT,
        created_by INTEGER,
        FOREIGN KEY (id) REFERENCES cards(id)
    )
    ''')
    
    # Create places table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS places (
        id INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (id) REFERENCES cards(id)
    )
    ''')
    
    # Create time_periods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_periods (
        id INTEGER PRIMARY KEY,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        FOREIGN KEY (id) REFERENCES cards(id)
    )
    ''')
    
    # Create days table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS days (
        id INTEGER PRIMARY KEY,
        date TIMESTAMP NOT NULL,
        FOREIGN KEY (id) REFERENCES cards(id)
    )
    ''')
    
    # Create years table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS years (
        id INTEGER PRIMARY KEY,
        year INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES cards(id)
    )
    ''')
    
    # Create media table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create junction tables for many-to-many relationships
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_people (
        event_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (event_id, person_id),
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (person_id) REFERENCES people(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_places (
        event_id INTEGER,
        place_id INTEGER,
        PRIMARY KEY (event_id, place_id),
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (place_id) REFERENCES places(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_time_periods (
        event_id INTEGER,
        time_period_id INTEGER,
        PRIMARY KEY (event_id, time_period_id),
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (time_period_id) REFERENCES time_periods(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory_people (
        memory_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (memory_id, person_id),
        FOREIGN KEY (memory_id) REFERENCES memories(id),
        FOREIGN KEY (person_id) REFERENCES people(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory_places (
        memory_id INTEGER,
        place_id INTEGER,
        PRIMARY KEY (memory_id, place_id),
        FOREIGN KEY (memory_id) REFERENCES memories(id),
        FOREIGN KEY (place_id) REFERENCES places(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory_time_periods (
        memory_id INTEGER,
        time_period_id INTEGER,
        PRIMARY KEY (memory_id, time_period_id),
        FOREIGN KEY (memory_id) REFERENCES memories(id),
        FOREIGN KEY (time_period_id) REFERENCES time_periods(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory_events (
        memory_id INTEGER,
        event_id INTEGER,
        PRIMARY KEY (memory_id, event_id),
        FOREIGN KEY (memory_id) REFERENCES memories(id),
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS card_media (
        card_id INTEGER,
        card_type TEXT NOT NULL,
        media_id INTEGER,
        PRIMARY KEY (card_id, card_type, media_id),
        FOREIGN KEY (card_id) REFERENCES cards(id),
        FOREIGN KEY (media_id) REFERENCES media(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 