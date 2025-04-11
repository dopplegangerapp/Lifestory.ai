from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

# Create database engine
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./app.db')
engine = create_engine(DATABASE_URL)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully") 