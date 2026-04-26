from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_URL = os.getenv("POSTGRES_URL")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)

def get_postgres_db():
    return SessionLocal()
