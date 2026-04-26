from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

MYSQL_URL = os.getenv("MYSQL_URL")

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(bind=engine)

def get_mysql_db():
    return SessionLocal()
