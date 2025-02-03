from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    MetaData,
    Boolean
)
from app.entity import Base
  
class IngestDocument(Base):  
    __tablename__ = "ingest_documents"  
    id = Column(Integer, primary_key=True, index=True) 
    ingest_code = Column(String, unique=True)
    file_path = Column(String, unique=True)  
    overlap = Column(Integer)
    chunk = Column(Integer)
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  