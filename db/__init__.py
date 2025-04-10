from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Create the database engine
engine = create_engine('sqlite:///droe_core.db', echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(db_url: str = "sqlite:///droecore.db"):
    """Initialize database connection and create tables"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
