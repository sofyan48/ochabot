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
  
class Client(Base):  
    __tablename__ = "clients"  
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    api_key = Column(String, unique=True)  
    secret_key = Column(String, unique=True)
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "api_key": self.api_key,
            "secret_key": self.secret_key,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }