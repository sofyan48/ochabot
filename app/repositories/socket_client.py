from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession    
from sqlalchemy import select, insert, delete, update    
from typing import Optional    
from datetime import datetime  
from app.entity.client_socket import ClientSocket  
  
class ClientSocketService:    
    def __init__(self, engine: AsyncEngine):    
        self.engine = engine    
            
    async def fetch(self, id: int) -> Optional[dict]:    
        query = select(ClientSocket).where(ClientSocket.id == id)    
        async with AsyncSession(self.engine) as session:    
            try:    
                result = await session.execute(query)    
                row = result.scalar_one_or_none()  
                return dict(row) if row else None  
            except Exception as e:    
                raise e    
                
    async def insert(self, name: str, secret: str) -> int:      
        query = insert(ClientSocket).values(name=name, secret=secret, created_at=datetime.now(), updated_at=datetime.now())      
        async with AsyncSession(self.engine) as session:      
            try:      
                result = await session.execute(query)      
                await session.commit()    
                return result.inserted_primary_key[0]    
            except Exception as e:      
                await session.rollback()    
                raise e      
  
    async def update(self, id: int, name: str, secret: str) -> bool:  
        query = (  
            update(ClientSocket)  
            .where(ClientSocket.id == id)  
            .values(name=name, secret=secret, updated_at=datetime.now())  
        )  
        async with AsyncSession(self.engine) as session:  
            try:  
                result = await session.execute(query)  
                await session.commit()  
                return result.rowcount > 0  
            except Exception as e:  
                await session.rollback()  
                raise e  
  
    async def delete(self, id: int) -> bool:  
        query = delete(ClientSocket).where(ClientSocket.id == id)  
        async with AsyncSession(self.engine) as session:  
            try:  
                result = await session.execute(query)  
                await session.commit()  
                return result.rowcount > 0  
            except Exception as e:  
                await session.rollback()  
                raise e  
