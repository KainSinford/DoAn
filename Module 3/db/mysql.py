from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import settings

engine = create_engine(settings.MYSQL_URL)
SessionLocal = sessionmaker(bind=engine)

def get_mysql_db():
    return SessionLocal()
