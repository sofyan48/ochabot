from sqlalchemy import Column, Integer, String, DateTime, MetaData  
from app.entity import Base
from datetime import datetime
  
class ClientSocket(Base):  
    __tablename__ = "client_sockets"  
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)  
    secret = Column(String)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "secret": self.secret,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }