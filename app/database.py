from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings

DATABASE_URL = settings.DATABASE_URL

# Tworzenie silnika SQLAlchemy do połączenia z bazą danych
engine = create_engine(DATABASE_URL)

# Tworzenie sesji SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
