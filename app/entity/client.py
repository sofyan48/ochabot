from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
  
class Client(Base):  
    __tablename__ = "clients"  
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    api_key = Column(String, unique=True)  
    secret_key = Column(String, unique=True)
    name = Column(String)
    is_active = Column(Boolean)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  