import sqlite3
from datetime import datetime
import json
from typing import Optional, Dict
import os
import logging

logger = logging.getLogger(__name__)

class SessionDB:
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _get_connection(self):
        """Get a database connection, creating one if necessary"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.conn

    def _init_db(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

    def save_session(self, session_id: str, data: Dict) -> None:
        """Save session data to the database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            # First check if session exists
            cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # Update existing session
                cursor.execute("""
                    UPDATE sessions 
                    SET data = ?, updated_at = ?
                    WHERE session_id = ?
                """, (json.dumps(data), datetime.now().isoformat(), session_id))
            else:
                # Insert new session
                cursor.execute("""
                    INSERT INTO sessions (session_id, data, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (session_id, json.dumps(data), datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            logger.info(f"Saved session {session_id}: {data}")
        except sqlite3.Error as e:
            logger.error(f"Error saving session {session_id}: {str(e)}")
            raise

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session data from the database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM sessions WHERE session_id = ?", (session_id,))
            result = cursor.fetchone()
            if result:
                data = json.loads(result[0])
                logger.info(f"Retrieved session {session_id}: {data}")
                return data
            logger.info(f"No session found for ID: {session_id}")
            return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving session {session_id}: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding session data for {session_id}: {str(e)}")
            return None

    def delete_session(self, session_id: str) -> None:
        """Delete a session from the database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
            logger.info(f"Deleted session {session_id}")
        except sqlite3.Error as e:
            logger.error(f"Error deleting session {session_id}: {str(e)}")
            raise

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        """Close database connection when object is destroyed"""
        self.close()

# Create a global instance
session_db = SessionDB() 