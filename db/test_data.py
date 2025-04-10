from db import SessionLocal
from db.models import EventModel, LocationModel, PersonModel, EmotionModel
from datetime import datetime

def create_test_data():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(EventModel).delete()
        db.query(LocationModel).delete()
        db.query(PersonModel).delete()
        db.query(EmotionModel).delete()
        
        # Create sample people
        people = [
            PersonModel(
                id=str(uuid.uuid4()),
                image_path="/images/person1.jpg",
                name="John Doe",
                relationship="Friend"
            ),
            PersonModel(
                id=str(uuid.uuid4()),
                image_path="/images/person2.jpg",
                name="Jane Smith",
                relationship="Colleague"
            )
        ]
        
        # Create sample emotions
        emotions = [
            EmotionModel(
                id=str(uuid.uuid4()),
                image_path="/images/happy.jpg",
                name="Happiness",
                intensity=8
            )
        ]
        
        # Create sample locations
        locations = [
            LocationModel(
                id=str(uuid.uuid4()),
                image_path="/images/beach.jpg",
                name="Beach"
            )
        ]
        
        # Create sample events
        events = [
            EventModel(
                id=str(uuid.uuid4()),
                image_path="/images/party.jpg",
                title="Birthday Party",
                description="John's 30th birthday celebration",
                people_data=[{"id": people[0].id, "name": people[0].name}, {"id": people[1].id, "name": people[1].name}],
                emotions_data=[{"id": emotions[0].id, "name": emotions[0].name}],
                location_data={"id": locations[0].id, "name": locations[0].name}
            )
        ]
        
        # Add all to database
        db.add_all(people + emotions + locations + events)
        db.commit()
        
        print("Successfully added test data")
    except Exception as e:
        db.rollback()
        print(f"Error adding test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import uuid
    create_test_data()
