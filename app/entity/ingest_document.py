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
  
class IngestDocument(Base):  
    __tablename__ = "ingest_documents"  
    id = Column(Integer, primary_key=True, index=True) 
    ingest_code = Column(String, unique=True)
    file_path = Column(String, unique=True)  
    overlap = Column(Integer)
    chunk = Column(Integer)
    is_build = Column(Boolean)
    collection = Column(String)
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),  # Pastikan id ada jika sudah disimpan
            "ingest_code": self.ingest_code,
            "file_path": self.file_path,
            "overlap": self.overlap,
            "chunk": self.chunk,
            "is_build": self.is_build,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }