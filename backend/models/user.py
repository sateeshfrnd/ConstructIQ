from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)