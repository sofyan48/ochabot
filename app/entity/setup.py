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
  
class Config(Base):  
    __tablename__ = "configs"  
    id = Column(Integer, primary_key=True, index=True)  
    key = Column(String, index=True)  
    value = Column(String)  
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }