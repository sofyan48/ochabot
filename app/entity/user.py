from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
from datetime import datetime
  
class User(Base):  
    __tablename__ = "users"  
    id = Column(Integer, primary_key=True, index=True) 
    email = Column(String, unique=True)
    username = Column(String, unique=True)  
    password = Column(String)
    name = Column(String)
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        try:
            return {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "name": self.name,
                "is_active": self.is_active,
                "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
                "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
            }
        except Exception as e:
            raise ValueError(f"Error converting User to dict: {str(e)}")