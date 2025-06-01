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
  
class Prompt(Base):  
    __tablename__ = "prompts"  
    id = Column(Integer, primary_key=True, index=True)  
    prompt = Column(String)
    scope_id = Column(Integer, index=True)
    is_default = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }