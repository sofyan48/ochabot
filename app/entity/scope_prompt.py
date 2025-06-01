from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime,
)
from app.entity import Base
from datetime import datetime
  
class ScopePrompts(Base):  
    __tablename__ = "scope_prompts"  
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True) 
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }