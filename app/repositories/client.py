    
from pkg.database.alchemy import select, or_
from typing import Optional    
from app.repositories import alchemy
from app.entity.client import Client  
from pkg import utils
  
class ClientRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = Client.__table__ 
                            
    async def upsert(self, data: dict) -> int:   
        try:
            return await self.engine.upsert_without_tx(
                model=Client, 
                values=data,
                conflict_key=["id"]
            )
        except Exception as e:
            raise e
    
    async def fetch(self, limit=10, page=1):
        offset = utils.offset(limit=limit, page=page)
        try:
            query = select(self.table).limit(limit=limit).offset(offset=offset)
            return await self.engine.find(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
        
    async def fetch_row(self, id):
        try:
            query = select(self.table).where(Client.id==id)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def fetch_row_by_apikey(self, apikey: str):
        print(apikey)
        try:
            query = select(self.table).where(Client.api_key==apikey)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def delete(self, id: int) -> bool: 
        return await self.engine.delete_without_tx(
            table=self.table,
            where_clause=(Client.id == id)
        ) 
    
    async def verify_apikey(self, apikey:str):
        try:
            query = select(self.table).where(Client.api_key==apikey)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e