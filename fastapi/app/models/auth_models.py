from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.infra.database import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., "admin", "student" 

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)   # e.g., "system", "user", "module" etc.
    group = Column(String, nullable=False)  # logical grouping
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)