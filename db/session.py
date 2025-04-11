import sqlite3
from contextlib import contextmanager
from typing import Generator, Any
import logging
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base class for database errors."""
    pass

class DatabaseConnectionError(DatabaseError):
    """Error connecting to the database."""
    pass

class DatabaseOperationError(DatabaseError):
    """Error performing database operations."""
    pass

@contextmanager
def get_db_session() -> Generator[sqlite3.Connection, None, None]:
    """Get a database session with automatic connection management."""
    conn = None
    try:
        conn = sqlite3.connect('droecore.db')
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise DatabaseConnectionError(f"Could not connect to database: {str(e)}")
    finally:
        if conn:
            try:
                conn.close()
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection: {str(e)}")

def save_card(card: Any) -> int:
    """Save a card to the database.
    
    Args:
        card: The card object to save
        
    Returns:
        int: The ID of the saved card
        
    Raises:
        DatabaseOperationError: If there's an error saving the card
    """
    try:
        with get_db_session() as conn:
            cursor = conn.cursor()
            
            # Start transaction
            conn.execute("BEGIN")
            
            try:
                # Insert into base cards table
                cursor.execute("""
                    INSERT INTO cards (title, description, created_at, updated_at, metadata, image_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    card.title,
                    card.description,
                    card.created_at.isoformat(),
                    card.updated_at.isoformat() if card.updated_at else None,
                    str(card.metadata) if card.metadata else None,
                    card.image_path
                ))
                
                card_id = cursor.lastrowid
                
                # Insert card-specific data based on type
                if isinstance(card, MemoryCard):
                    cursor.execute("""
                        INSERT INTO memories (id, date, emotion, intensity)
                        VALUES (?, ?, ?, ?)
                    """, (
                        card_id,
                        card.date.isoformat() if card.date else None,
                        card.emotion,
                        card.intensity
                    ))
                elif isinstance(card, PersonCard):
                    cursor.execute("""
                        INSERT INTO people (id, relationship, created_by)
                        VALUES (?, ?, ?)
                    """, (
                        card_id,
                        card.relationships[0] if card.relationships else None,
                        card.created_by
                    ))
                elif isinstance(card, PlaceCard):
                    cursor.execute("""
                        INSERT INTO places (id, latitude, longitude)
                        VALUES (?, ?, ?)
                    """, (
                        card_id,
                        card.latitude,
                        card.longitude
                    ))
                else:
                    raise DatabaseOperationError(f"Unsupported card type: {type(card)}")
                
                # Save media if any
                for media in card.media:
                    cursor.execute("""
                        INSERT INTO media (file_path, type, description, created_at)
                        VALUES (?, ?, ?, ?)
                    """, (
                        media.file_path,
                        media.type,
                        media.description,
                        media.created_at.isoformat()
                    ))
                    media_id = cursor.lastrowid
                    
                    cursor.execute("""
                        INSERT INTO card_media (card_id, card_type, media_id)
                        VALUES (?, ?, ?)
                    """, (
                        card_id,
                        type(card).__name__,
                        media_id
                    ))
                
                conn.commit()
                return card_id
                
            except Exception as e:
                conn.rollback()
                logger.error(f"Error saving card: {str(e)}")
                raise DatabaseOperationError(f"Failed to save card: {str(e)}")
                
    except DatabaseConnectionError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving card: {str(e)}")
        raise DatabaseOperationError(f"Unexpected error saving card: {str(e)}") 