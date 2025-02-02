from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
  
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