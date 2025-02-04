    
from pkg.database.alchemy import select, desc
from typing import Optional    
from app.repositories import alchemy
from app.entity.client_socket import ClientSocket  
from pkg import utils
  
class ClientSocketRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = ClientSocket.__table__ 
            
    async def fetch(self, id: int) -> Optional[dict]:    
        query = select(ClientSocket).where(ClientSocket.id == id)    
        return await self.engine.fetch(query=query)
                
    async def upsert(self, data: dict) -> int:   
        try:
            return await self.engine.upsert_without_tx(
                model=ClientSocket, 
                values=data,
                conflict_key=['id']
            )
        except Exception as e:
            raise e
    
    async def list(self, limit=10, page=1):
        offset = utils.offset(limit=limit, page=page)
        try:
            query = select(self.table).limit(limit=limit).offset(offset=offset).order_by(desc(ClientSocket.id))
            return await self.engine.find(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
        
    async def fetch(self, id):
        try:
            query = select(self.table).where(ClientSocket.id==id)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def delete(self, id: int) -> bool: 
        return await self.engine.delete_without_tx(
            table=ClientSocket.__tablename__,
            where_clause=(ClientSocket.id == id)
        ) 
