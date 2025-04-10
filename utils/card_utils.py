from typing import Union, Dict, Any, List, Optional, Type, TypeVar
from cards.base_card import BaseCard
from cards.event_card import EventCard
from cards.location_card import LocationCard
from cards.person_card import PersonCard
from cards.emotion_card import EmotionCard
from cards.memory_card import MemoryCard
from cards.place_card import PlaceCard
from cards.time_period_card import TimePeriodCard
from cards.day_card import DayCard
from cards.year_card import YearCard
from cards.media import Media
import uuid
from datetime import datetime
import sqlite3

T = TypeVar('T', bound=BaseCard)

class CardUtils:
    """Utility functions for working with cards in the DROE Core system."""
    
    def __init__(self, db_path: str = 'droecore.db'):
        self.db_path = db_path
    
    def get_db(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def save_card(self, card: BaseCard) -> int:
        """Save a card to the database and return its ID"""
        conn = self.get_db()
        cursor = conn.cursor()
        
        try:
            # Save the base card data
            cursor.execute('''
                INSERT INTO cards (title, description, created_at)
                VALUES (?, ?, ?)
            ''', (card.title, card.description, card.created_at))
            
            card_id = cursor.lastrowid
            
            # Save card-specific data
            if isinstance(card, EventCard):
                self._save_event_card(cursor, card_id, card)
            elif isinstance(card, MemoryCard):
                self._save_memory_card(cursor, card_id, card)
            elif isinstance(card, PersonCard):
                self._save_person_card(cursor, card_id, card)
            elif isinstance(card, PlaceCard):
                self._save_place_card(cursor, card_id, card)
            elif isinstance(card, TimePeriodCard):
                self._save_time_period_card(cursor, card_id, card)
            elif isinstance(card, DayCard):
                self._save_day_card(cursor, card_id, card)
            elif isinstance(card, YearCard):
                self._save_year_card(cursor, card_id, card)
            
            # Save relationships
            self._save_card_relationships(cursor, card_id, card)
            
            # Save media
            self._save_card_media(cursor, card_id, card)
            
            conn.commit()
            return card_id
            
        finally:
            conn.close()
    
    def get_card(self, card_id: int, card_type: Type[T]) -> Optional[T]:
        """Get a card by ID and type"""
        conn = self.get_db()
        cursor = conn.cursor()
        
        try:
            # Get base card data
            cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
            card_data = cursor.fetchone()
            
            if not card_data:
                return None
            
            # Get card-specific data
            if card_type == EventCard:
                return self._get_event_card(cursor, card_id)
            elif card_type == MemoryCard:
                return self._get_memory_card(cursor, card_id)
            elif card_type == PersonCard:
                return self._get_person_card(cursor, card_id)
            elif card_type == PlaceCard:
                return self._get_place_card(cursor, card_id)
            elif card_type == TimePeriodCard:
                return self._get_time_period_card(cursor, card_id)
            elif card_type == DayCard:
                return self._get_day_card(cursor, card_id)
            elif card_type == YearCard:
                return self._get_year_card(cursor, card_id)
            
            return None
            
        finally:
            conn.close()
    
    def get_cards_by_type(self, card_type: Type[T]) -> List[T]:
        """Get all cards of a specific type"""
        conn = self.get_db()
        cursor = conn.cursor()
        
        try:
            if card_type == EventCard:
                return self._get_all_event_cards(cursor)
            elif card_type == MemoryCard:
                return self._get_all_memory_cards(cursor)
            elif card_type == PersonCard:
                return self._get_all_person_cards(cursor)
            elif card_type == PlaceCard:
                return self._get_all_place_cards(cursor)
            elif card_type == TimePeriodCard:
                return self._get_all_time_period_cards(cursor)
            elif card_type == DayCard:
                return self._get_all_day_cards(cursor)
            elif card_type == YearCard:
                return self._get_all_year_cards(cursor)
            
            return []
            
        finally:
            conn.close()
    
    def _save_event_card(self, cursor: sqlite3.Cursor, card_id: int, card: EventCard):
        """Save event card specific data"""
        cursor.execute('''
            INSERT INTO events (id, start_date, end_date)
            VALUES (?, ?, ?)
        ''', (card_id, card.start_date, card.end_date))
    
    def _save_memory_card(self, cursor: sqlite3.Cursor, card_id: int, card: MemoryCard):
        """Save memory card specific data"""
        cursor.execute('''
            INSERT INTO memories (id, date, emotion, intensity)
            VALUES (?, ?, ?, ?)
        ''', (card_id, card.date, card.emotion, card.intensity))
    
    def _save_person_card(self, cursor: sqlite3.Cursor, card_id: int, card: PersonCard):
        """Save person card specific data"""
        cursor.execute('''
            INSERT INTO people (id, relationship)
            VALUES (?, ?)
        ''', (card_id, card.relationship))
    
    def _save_place_card(self, cursor: sqlite3.Cursor, card_id: int, card: PlaceCard):
        """Save place card specific data"""
        cursor.execute('''
            INSERT INTO places (id, latitude, longitude)
            VALUES (?, ?, ?)
        ''', (card_id, card.latitude, card.longitude))
    
    def _save_time_period_card(self, cursor: sqlite3.Cursor, card_id: int, card: TimePeriodCard):
        """Save time period card specific data"""
        cursor.execute('''
            INSERT INTO time_periods (id, start_date, end_date)
            VALUES (?, ?, ?)
        ''', (card_id, card.start_date, card.end_date))
    
    def _save_day_card(self, cursor: sqlite3.Cursor, card_id: int, card: DayCard):
        """Save day card specific data"""
        cursor.execute('''
            INSERT INTO days (id, date)
            VALUES (?, ?)
        ''', (card_id, card.date))
    
    def _save_year_card(self, cursor: sqlite3.Cursor, card_id: int, card: YearCard):
        """Save year card specific data"""
        cursor.execute('''
            INSERT INTO years (id, year)
            VALUES (?, ?)
        ''', (card_id, card.year))
    
    def _save_card_relationships(self, cursor: sqlite3.Cursor, card_id: int, card: BaseCard):
        """Save card relationships"""
        if isinstance(card, EventCard):
            for person in card.people:
                cursor.execute('''
                    INSERT INTO event_people (event_id, person_id)
                    VALUES (?, ?)
                ''', (card_id, person.id))
            
            if card.location:
                cursor.execute('''
                    INSERT INTO event_places (event_id, place_id)
                    VALUES (?, ?)
                ''', (card_id, card.location.id))
            
            if card.time_period:
                cursor.execute('''
                    INSERT INTO event_time_periods (event_id, time_period_id)
                    VALUES (?, ?)
                ''', (card_id, card.time_period.id))
        
        elif isinstance(card, MemoryCard):
            for person in card.associated_people:
                cursor.execute('''
                    INSERT INTO memory_people (memory_id, person_id)
                    VALUES (?, ?)
                ''', (card_id, person.id))
            
            if card.associated_place:
                cursor.execute('''
                    INSERT INTO memory_places (memory_id, place_id)
                    VALUES (?, ?)
                ''', (card_id, card.associated_place.id))
            
            if card.associated_time_period:
                cursor.execute('''
                    INSERT INTO memory_time_periods (memory_id, time_period_id)
                    VALUES (?, ?)
                ''', (card_id, card.associated_time_period.id))
            
            if card.associated_event:
                cursor.execute('''
                    INSERT INTO memory_events (memory_id, event_id)
                    VALUES (?, ?)
                ''', (card_id, card.associated_event.id))
    
    def _save_card_media(self, cursor: sqlite3.Cursor, card_id: int, card: BaseCard):
        """Save card media"""
        for media in card.media:
            cursor.execute('''
                INSERT INTO media (file_path, type, description)
                VALUES (?, ?, ?)
            ''', (media.file_path, media.type.value, media.description))
            
            media_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO card_media (card_id, card_type, media_id)
                VALUES (?, ?, ?)
            ''', (card_id, type(card).__name__, media_id))
    
    def _get_event_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[EventCard]:
        """Get event card by ID"""
        cursor.execute('''
            SELECT c.*, e.start_date, e.end_date
            FROM cards c
            JOIN events e ON c.id = e.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = EventCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            start_date=datetime.fromisoformat(data[4]),
            end_date=datetime.fromisoformat(data[5]) if data[5] else None
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_memory_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[MemoryCard]:
        """Get memory card by ID"""
        cursor.execute('''
            SELECT c.*, m.date, m.emotion, m.intensity
            FROM cards c
            JOIN memories m ON c.id = m.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = MemoryCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            date=datetime.fromisoformat(data[4]),
            emotion=data[5],
            intensity=data[6]
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_person_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[PersonCard]:
        """Get person card by ID"""
        cursor.execute('''
            SELECT c.*, p.relationship
            FROM cards c
            JOIN people p ON c.id = p.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = PersonCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            relationship=data[4]
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_place_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[PlaceCard]:
        """Get place card by ID"""
        cursor.execute('''
            SELECT c.*, p.latitude, p.longitude
            FROM cards c
            JOIN places p ON c.id = p.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = PlaceCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            latitude=data[4],
            longitude=data[5]
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_time_period_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[TimePeriodCard]:
        """Get time period card by ID"""
        cursor.execute('''
            SELECT c.*, tp.start_date, tp.end_date
            FROM cards c
            JOIN time_periods tp ON c.id = tp.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = TimePeriodCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            start_date=datetime.fromisoformat(data[4]),
            end_date=datetime.fromisoformat(data[5]) if data[5] else None
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_day_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[DayCard]:
        """Get day card by ID"""
        cursor.execute('''
            SELECT c.*, d.date
            FROM cards c
            JOIN days d ON c.id = d.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = DayCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            date=datetime.fromisoformat(data[4])
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_year_card(self, cursor: sqlite3.Cursor, card_id: int) -> Optional[YearCard]:
        """Get year card by ID"""
        cursor.execute('''
            SELECT c.*, y.year
            FROM cards c
            JOIN years y ON c.id = y.id
            WHERE c.id = ?
        ''', (card_id,))
        
        data = cursor.fetchone()
        if not data:
            return None
        
        card = YearCard(
            id=data[0],
            title=data[1],
            description=data[2],
            created_at=datetime.fromisoformat(data[3]),
            year=data[4]
        )
        
        # Get related data
        self._get_card_relationships(cursor, card)
        self._get_card_media(cursor, card)
        
        return card
    
    def _get_card_relationships(self, cursor: sqlite3.Cursor, card: BaseCard):
        """Get card relationships"""
        if isinstance(card, EventCard):
            # Get people
            cursor.execute('''
                SELECT p.*
                FROM people p
                JOIN event_people ep ON p.id = ep.person_id
                WHERE ep.event_id = ?
            ''', (card.id,))
            
            for person_data in cursor.fetchall():
                person = PersonCard(
                    id=person_data[0],
                    title=person_data[1],
                    description=person_data[2],
                    created_at=datetime.fromisoformat(person_data[3]),
                    relationship=person_data[4]
                )
                card.people.append(person)
            
            # Get location
            cursor.execute('''
                SELECT p.*
                FROM places p
                JOIN event_places ep ON p.id = ep.place_id
                WHERE ep.event_id = ?
            ''', (card.id,))
            
            place_data = cursor.fetchone()
            if place_data:
                card.location = PlaceCard(
                    id=place_data[0],
                    title=place_data[1],
                    description=place_data[2],
                    created_at=datetime.fromisoformat(place_data[3]),
                    latitude=place_data[4],
                    longitude=place_data[5]
                )
            
            # Get time period
            cursor.execute('''
                SELECT tp.*
                FROM time_periods tp
                JOIN event_time_periods etp ON tp.id = etp.time_period_id
                WHERE etp.event_id = ?
            ''', (card.id,))
            
            time_period_data = cursor.fetchone()
            if time_period_data:
                card.time_period = TimePeriodCard(
                    id=time_period_data[0],
                    title=time_period_data[1],
                    description=time_period_data[2],
                    created_at=datetime.fromisoformat(time_period_data[3]),
                    start_date=datetime.fromisoformat(time_period_data[4]),
                    end_date=datetime.fromisoformat(time_period_data[5]) if time_period_data[5] else None
                )
        
        elif isinstance(card, MemoryCard):
            # Get people
            cursor.execute('''
                SELECT p.*
                FROM people p
                JOIN memory_people mp ON p.id = mp.person_id
                WHERE mp.memory_id = ?
            ''', (card.id,))
            
            for person_data in cursor.fetchall():
                person = PersonCard(
                    id=person_data[0],
                    title=person_data[1],
                    description=person_data[2],
                    created_at=datetime.fromisoformat(person_data[3]),
                    relationship=person_data[4]
                )
                card.associated_people.append(person)
            
            # Get place
            cursor.execute('''
                SELECT p.*
                FROM places p
                JOIN memory_places mp ON p.id = mp.place_id
                WHERE mp.memory_id = ?
            ''', (card.id,))
            
            place_data = cursor.fetchone()
            if place_data:
                card.associated_place = PlaceCard(
                    id=place_data[0],
                    title=place_data[1],
                    description=place_data[2],
                    created_at=datetime.fromisoformat(place_data[3]),
                    latitude=place_data[4],
                    longitude=place_data[5]
                )
            
            # Get time period
            cursor.execute('''
                SELECT tp.*
                FROM time_periods tp
                JOIN memory_time_periods mtp ON tp.id = mtp.time_period_id
                WHERE mtp.memory_id = ?
            ''', (card.id,))
            
            time_period_data = cursor.fetchone()
            if time_period_data:
                card.associated_time_period = TimePeriodCard(
                    id=time_period_data[0],
                    title=time_period_data[1],
                    description=time_period_data[2],
                    created_at=datetime.fromisoformat(time_period_data[3]),
                    start_date=datetime.fromisoformat(time_period_data[4]),
                    end_date=datetime.fromisoformat(time_period_data[5]) if time_period_data[5] else None
                )
            
            # Get event
            cursor.execute('''
                SELECT e.*
                FROM events e
                JOIN memory_events me ON e.id = me.event_id
                WHERE me.memory_id = ?
            ''', (card.id,))
            
            event_data = cursor.fetchone()
            if event_data:
                card.associated_event = EventCard(
                    id=event_data[0],
                    title=event_data[1],
                    description=event_data[2],
                    created_at=datetime.fromisoformat(event_data[3]),
                    start_date=datetime.fromisoformat(event_data[4]),
                    end_date=datetime.fromisoformat(event_data[5]) if event_data[5] else None
                )
    
    def _get_card_media(self, cursor: sqlite3.Cursor, card: BaseCard):
        """Get card media"""
        cursor.execute('''
            SELECT m.*
            FROM media m
            JOIN card_media cm ON m.id = cm.media_id
            WHERE cm.card_id = ? AND cm.card_type = ?
        ''', (card.id, type(card).__name__))
        
        for media_data in cursor.fetchall():
            media = Media(
                id=media_data[0],
                file_path=media_data[1],
                type=media_data[2],
                created_at=datetime.fromisoformat(media_data[3]),
                description=media_data[4]
            )
            card.media.append(media)
    
    def _get_all_event_cards(self, cursor: sqlite3.Cursor) -> List[EventCard]:
        """Get all event cards"""
        cursor.execute('''
            SELECT c.*, e.start_date, e.end_date
            FROM cards c
            JOIN events e ON c.id = e.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = EventCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                start_date=datetime.fromisoformat(data[4]),
                end_date=datetime.fromisoformat(data[5]) if data[5] else None
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_memory_cards(self, cursor: sqlite3.Cursor) -> List[MemoryCard]:
        """Get all memory cards"""
        cursor.execute('''
            SELECT c.*, m.date, m.emotion, m.intensity
            FROM cards c
            JOIN memories m ON c.id = m.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = MemoryCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                date=datetime.fromisoformat(data[4]),
                emotion=data[5],
                intensity=data[6]
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_person_cards(self, cursor: sqlite3.Cursor) -> List[PersonCard]:
        """Get all person cards"""
        cursor.execute('''
            SELECT c.*, p.relationship
            FROM cards c
            JOIN people p ON c.id = p.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = PersonCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                relationship=data[4]
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_place_cards(self, cursor: sqlite3.Cursor) -> List[PlaceCard]:
        """Get all place cards"""
        cursor.execute('''
            SELECT c.*, p.latitude, p.longitude
            FROM cards c
            JOIN places p ON c.id = p.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = PlaceCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                latitude=data[4],
                longitude=data[5]
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_time_period_cards(self, cursor: sqlite3.Cursor) -> List[TimePeriodCard]:
        """Get all time period cards"""
        cursor.execute('''
            SELECT c.*, tp.start_date, tp.end_date
            FROM cards c
            JOIN time_periods tp ON c.id = tp.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = TimePeriodCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                start_date=datetime.fromisoformat(data[4]),
                end_date=datetime.fromisoformat(data[5]) if data[5] else None
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_day_cards(self, cursor: sqlite3.Cursor) -> List[DayCard]:
        """Get all day cards"""
        cursor.execute('''
            SELECT c.*, d.date
            FROM cards c
            JOIN days d ON c.id = d.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = DayCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                date=datetime.fromisoformat(data[4])
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards
    
    def _get_all_year_cards(self, cursor: sqlite3.Cursor) -> List[YearCard]:
        """Get all year cards"""
        cursor.execute('''
            SELECT c.*, y.year
            FROM cards c
            JOIN years y ON c.id = y.id
        ''')
        
        cards = []
        for data in cursor.fetchall():
            card = YearCard(
                id=data[0],
                title=data[1],
                description=data[2],
                created_at=datetime.fromisoformat(data[3]),
                year=data[4]
            )
            
            # Get related data
            self._get_card_relationships(cursor, card)
            self._get_card_media(cursor, card)
            
            cards.append(card)
        
        return cards

def validate_card(card: Union[BaseCard, EventCard, LocationCard, PersonCard, EmotionCard]) -> bool:
    """Validate card structure and required fields"""
    if not isinstance(card, BaseCard):
        return False
    
    # All cards must have an image
    if not hasattr(card, 'image_path') or not card.image_path:
        return False
        
    # Check card type specific requirements
    if isinstance(card, EventCard):
        required = ['title', 'description', 'location', 'people', 'emotions', 'memories']
    elif isinstance(card, LocationCard):
        required = ['name', 'events', 'memories']
    elif isinstance(card, PersonCard):
        required = ['name', 'relationship', 'events', 'memories']
    elif isinstance(card, EmotionCard):
        required = ['name', 'intensity', 'memories']
    else:  # BaseCard
        required = []
        
    return all(hasattr(card, field) and getattr(card, field) for field in required)

def format_card_for_display(card: BaseCard) -> dict:
    """Format card data for UI display with expandable sections"""
    if not validate_card(card):
        raise ValueError("Invalid card structure")
    
    return {
        'id': generate_card_id(),
        'image': card.image_path,
        'data': card.expandable_data
    }

def generate_card_id() -> str:
    """Generate unique ID for new cards"""
    return str(uuid.uuid4())
