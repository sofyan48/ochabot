    
from pkg.database.alchemy import (
    AlChemy,
    select,
    where,
)
from typing import Optional    
from datetime import datetime  
from app.entity.client_socket import ClientSocket  
  
class ClientSocketRepositories:    
    def __init__(self, engine: AlChemy):    
        self.engine = engine    
            
    async def fetch(self, id: int) -> Optional[dict]:    
        query = select(ClientSocket).where(ClientSocket.id == id)    
        return await self.engine.fetch(query=query)
                
    async def insert(self, name: str, secret: str) -> int:      
        return await self.engine.insert_without_tx(ClientSocket.__tablename__, {
            "name": name, 
            "secret": secret,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
    
    async def update(self, name: str, secret: str) -> int:      
        return await self.engine.update_without_tx(table=ClientSocket.__tablename__, 
            values={
                "name": name, 
                "secret": secret,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            where_clause=(ClientSocket.id==id)
        )
  
    async def delete(self, id: int) -> bool: 
        return await self.engine.delete_without_tx(
            table=ClientSocket.__tablename__,
            where_clause=(ClientSocket.id == id)
        ) 
