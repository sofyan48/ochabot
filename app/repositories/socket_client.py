from pkg.database.alchemy import select, desc
from typing import Optional    
from app.repositories import alchemy
from app.entity.client_socket import ClientSocket  
from pkg import utils
from sqlalchemy.sql import func
  
class ClientSocketRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = ClientSocket.__table__ 
            
    async def fetch(self, id: int) -> Optional[dict]:    
        query = select(ClientSocket).where(ClientSocket.id == id)    
        return await self.engine.fetch(query=query)
                
    async def upsert(self, data: ClientSocket) -> int:   
        try:
            entity = {
                "name": data.name,
                "secret": data.secret,
                "created_at": data.created_at,
                "updated_at": data.updated_at,
            }
            if data.id is not None:
                entity["id"] = data.id
                
            return await self.engine.upsert_without_tx(
                model=ClientSocket, 
                values=entity,
                conflict_key=['id']
            )
        except Exception as e:
            raise e
    
    async def list(self, limit=10, page=1):
        offset = utils.offset(limit=limit, page=page)
        try:
            # Query dengan limit dan offset untuk pagination
            query = (
                select(self.table)
                .limit(limit)
                .offset(offset)
                .order_by(desc(ClientSocket.id))
            )
            results = await self.engine.find(query=query, arguments={})

            # Hitung total data untuk mengetahui jumlah halaman
            total_query = select(func.count(self.table.c.id))  # Menggunakan func.count untuk menghitung total baris
            total_count = await self.engine.count(query=total_query)

            # Hitung total halaman
            total_pages = (total_count + limit - 1) // limit

            return {
                "data": results,
                "pagination": {
                    "current_page": page,
                    "per_page": limit,
                    "total_pages": total_pages,
                    "total_items": total_count,
                },
            }
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
