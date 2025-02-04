    
from pkg.database.alchemy import select, or_, desc
from typing import Optional    
from app.repositories import alchemy
from app.entity.user import User  
from pkg import utils
  
class UserRepositories:    
    def __init__(self):    
        self.engine = alchemy   
        self.table = User.__table__ 
            
    async def fetch(self, id: int) -> Optional[dict]:    
        query = select(UserRepositories).where(UserRepositories.id == id)    
        return await self.engine.fetch(query=query)
                
    async def upsert(self, data: dict) -> int:   
        try:
            return await self.engine.upsert_without_tx(
                model=User, 
                values=data,
                conflict_key=["id"]
            )
        except Exception as e:
            raise e
    
    async def list(self, limit=10, page=1):
        offset = utils.offset(limit=limit, page=page)
        try:
            query = select(self.table).limit(limit=limit).offset(offset=offset).order_by(desc(User.id))
            return await self.engine.find(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
        
    async def fetch(self, id):
        try:
            query = select(self.table).where(User.id==id)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
    
    async def delete(self, id: int) -> bool: 
        return await self.engine.delete_without_tx(
            table=self.table,
            where_clause=(User.id == id)
        ) 
    
    async def get_by_username_or_email(self, username):
        try:
            query = select(self.table).where(or_(User.username==username, User.email==username), User.is_active==True)
            return await self.engine.fetch(
                query=query,
                arguments={}
            )
        except Exception as e:
            raise e
