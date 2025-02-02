from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
  
class Prompt(Base):  
    __tablename__ = "prompts"  
    id = Column(Integer, primary_key=True, index=True)  
    prompt = Column(String)
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  