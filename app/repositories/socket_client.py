from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import text, bindparam, insert
from typing import Optional, List
from sqlalchemy import select, and_, Table, Column, Integer, String, MetaData, DateTime

metadata = MetaData()

client_sockets = Table(
    "client_sockets",
    metadata,
    Column("id", Integer),
    Column("name", String),
    Column("secret", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)

class ClientSocket(object):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        
    async def fetch(self, id: int) -> Optional[dict]:
        query = (
            select(client_sockets).where(client_sockets.c.id == id)
        )            
        async with AsyncSession(self.engine) as session:
            try:
                result = await session.execute(query)
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows] if rows else []
            except Exception as e:
                raise e
            
    async def insert(self, name: str, secret: str) -> int:  
        query = insert(client_sockets).values(name=name, secret=secret)  
        async with AsyncSession(self.engine) as session:  
            try:  
                result = await session.execute(query)  
                await session.commit()
                return result.inserted_primary_key[0]
            except Exception as e:  
                await session.rollback()
                raise e  