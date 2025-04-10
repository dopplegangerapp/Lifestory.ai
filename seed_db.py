import sqlite3
from datetime import datetime, timedelta
import hashlib
from cards.event_card import EventCard
from cards.memory_card import MemoryCard
from cards.person_card import PersonCard
from cards.place_card import PlaceCard
from cards.time_period_card import TimePeriodCard
from cards.day_card import DayCard
from cards.year_card import YearCard
from utils.card_utils import CardUtils

def seed_db():
    """Seed the database with sample data."""
    # Initialize card utils
    card_utils = CardUtils()
    
    # Create sample people
    john = PersonCard(
        title="John Smith",
        description="Father figure and mentor",
        relationship="family"
    )
    sarah = PersonCard(
        title="Sarah Johnson",
        description="Best friend since college",
        relationship="friend"
    )
    mike = PersonCard(
        title="Mike Wilson",
        description="Project manager at work",
        relationship="colleague"
    )
    
    # Create sample places
    home = PlaceCard(
        title="Home",
        description="Childhood home in Seattle",
        latitude=47.6062,
        longitude=-122.3321
    )
    university = PlaceCard(
        title="University",
        description="Where I studied Computer Science",
        latitude=47.6553,
        longitude=-122.3035
    )
    central_park = PlaceCard(
        title="Central Park",
        description="Favorite spot for relaxation",
        latitude=40.7829,
        longitude=-73.9654
    )
    
    # Create sample time periods
    college_years = TimePeriodCard(
        title="College Years",
        description="My undergraduate studies",
        start_date=datetime(2018, 9, 1),
        end_date=datetime(2022, 6, 15)
    )
    
    # Create sample year
    graduation_year = YearCard(
        title="2022",
        description="The year I graduated",
        year=2022
    )
    
    # Create sample day
    graduation_day = DayCard(
        title="Graduation Day",
        description="The day I graduated from university",
        date=datetime(2022, 6, 15)
    )
    
    # Create sample events
    graduation = EventCard(
        title="Graduation Ceremony",
        description="Graduated with honors in Computer Science",
        start_date=datetime(2022, 6, 15, 14, 0),
        end_date=datetime(2022, 6, 15, 17, 0)
    )
    graduation.add_person(john)
    graduation.add_person(sarah)
    graduation.set_location(university)
    graduation.set_time_period(college_years)
    
    first_job = EventCard(
        title="First Day at Work",
        description="Started my career as a software developer",
        start_date=datetime(2022, 7, 1, 9, 0),
        end_date=datetime(2022, 7, 1, 17, 0)
    )
    first_job.add_person(mike)
    
    family_reunion = EventCard(
        title="Family Reunion",
        description="Annual family gathering at the lake house",
        start_date=datetime(2022, 8, 15, 12, 0),
        end_date=datetime(2022, 8, 17, 14, 0)
    )
    family_reunion.add_person(john)
    family_reunion.set_location(home)
    
    # Create sample memories
    first_code = MemoryCard(
        title="First Code",
        description="Writing my first 'Hello, World!' program",
        date=datetime(2018, 9, 15),
        emotion="excitement",
        intensity=8
    )
    first_code.add_person(john)
    first_code.set_place(university)
    first_code.set_time_period(college_years)
    first_code.set_event(graduation)
    
    team_celebration = MemoryCard(
        title="Team Celebration",
        description="Project completion celebration with the team",
        date=datetime(2022, 7, 15),
        emotion="pride",
        intensity=9
    )
    team_celebration.add_person(mike)
    team_celebration.set_event(first_job)
    
    family_photo = MemoryCard(
        title="Family Photo",
        description="Group photo at the reunion",
        date=datetime(2022, 8, 16),
        emotion="joy",
        intensity=10
    )
    family_photo.add_person(john)
    family_photo.set_place(home)
    family_photo.set_event(family_reunion)
    
    # Save all cards
    cards = [
        john, sarah, mike,
        home, university, central_park,
        college_years,
        graduation_year,
        graduation_day,
        graduation, first_job, family_reunion,
        first_code, team_celebration, family_photo
    ]
    
    for card in cards:
        card_utils.save_card(card)
    
    print("Database seeded successfully with sample cards!")

if __name__ == '__main__':
    seed_db() 