from pkg.database.alchemy import select, desc, asc
from app.repositories import alchemy
from app.entity.ingest_document import IngestDocument  
from pkg import utils
from sqlalchemy.sql import func
  
class IngestDocumentRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = IngestDocument.__table__ 
                            
    async def upsert(self, data: IngestDocument) -> int:   
        try:
            entity = {
                "ingest_code": data.ingest_code,
                "file_path": data.file_path,
                "overlap": data.overlap,
                "chunk": data.chunk,
                "created_at": data.created_at,
                "updated_at": data.updated_at,
                "is_build": data.is_build,
                "collection": data.collection,
            }
            
            if data.id is not None:
                entity["id"] = data.id

            return await self.engine.upsert_without_tx(
                model=IngestDocument, 
                values=entity,
                conflict_key=["id"]
            )
        except Exception as e:
            raise e
    
    async def fetch(self, limit=10, page=1):
        offset = utils.offset(limit=limit, page=page)
        try:
            # Query dengan limit dan offset untuk pagination
            query = select(self.table).limit(limit).offset(offset)
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
        
    async def fetch_row(self, id):
        try:
            query = select(self.table).where(IngestDocument.id==id)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e

    async def fetch_row_by_ingest_code(self, ingest_code):
        try:
            query = select(self.table).where(IngestDocument.ingest_code==ingest_code).order_by(desc(IngestDocument.id))
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def fetch_row_by_apikey(self, apikey: str):
        try:
            query = select(self.table).where(IngestDocument.api_key==apikey)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def delete(self, id: int) -> bool: 
        return await self.engine.delete_without_tx(
            table=self.table,
            where_clause=(IngestDocument.id == id)
        ) 
    
    async def verify_apikey(self, apikey:str):
        try:
            query = select(self.table).where(IngestDocument.api_key==apikey)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e