from sqlalchemy import Column, Integer, Boolean, String
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, index= True)
    description = Column(String, nullable =True)
    completed = Column(Boolean, default= False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index= True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)