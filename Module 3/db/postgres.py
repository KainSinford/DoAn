from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import settings

engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)

def get_postgres_db():
    return SessionLocal()
