from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
  
class Config(Base):  
    __tablename__ = "config"  
    id = Column(Integer, primary_key=True, index=True)  
    key = Column(String, index=True)  
    value = Column(String)  
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  