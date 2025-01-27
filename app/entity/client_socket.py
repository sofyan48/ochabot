from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData  
from sqlalchemy.ext.declarative import declarative_base  
  
Base = declarative_base()  
  
class ClientSocket(Base):  
    __tablename__ = "client_sockets"  
  
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)  
    secret = Column(String)  
    created_at = Column(DateTime)  
    updated_at = Column(DateTime)  