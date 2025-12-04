from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db") #base de datos local

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind= engine)

Base= declarative_base()

# Dependencia para obtener sesion en cada request
def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()