    
from pkg.database.alchemy import select    
from app.repositories import alchemy
from app.entity.ingest_document import IngestDocument  
from pkg import utils
  
class IngestDocumentRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = IngestDocument.__table__ 
                            
    async def upsert(self, data: dict) -> int:   
        try:
            return await self.engine.upsert_without_tx(
                model=IngestDocument, 
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
            query = select(self.table).where(IngestDocument.id==id)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e

    async def fetch_row_by_ingest_code(self, ingest_code):
        try:
            query = select(self.table).where(IngestDocument.ingest_code==ingest_code)
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