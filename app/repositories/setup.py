from app.repositories import redis, logger, alchemy
from app.entity.setup import Config
from pkg.database.alchemy import select

class SetupConfig(object):
    def __init__(self):
        self.redis = redis
        self.key = "config:"
        self.db = alchemy
        self.table = Config.__table__
        self.model_class = Config

    async def list_key(self):
        try:
            query = select(Config.__table__).where(Config.is_active == True)
            result = await self.db.find(query=query, arguments={})
            return result
        except Exception as e:
            raise
    

    async def platform(self, value):
        key = self.key+"llm:platform"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
          
    
    async def model(self, value):
        key = self.key+"llm:model"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
    
    async def top_k(self, value):
        key = self.key+"retriever:top_k"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
    
    async def fetch_k(self, value):
        key = self.key+"retriever:fetch_k"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
    
    async def collection(self, value):
        key = self.key+"retriever:collection"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
    
    async def vector_db(self, value):
        key = self.key+"retriever:vector_db"
        return await self.db.upsert_without_tx(self.model_class, {
            "key": key,
            "value": value,
            "is_active": True
        }, conflict_key="key")
    
    async def fetch(self, key):
        try:
            query = select(self.table).where(Config.key == key)    
            self.db.fetch(query=query, arguments={})
        except Exception as e:
            raise e
        
    async def get_all_setup(self):
        key = self.key+"*"
        try:
            keys = await self.redis.keys(key)
            key_value_pairs = {key: await self.redis.get(key) for key in keys}
            return  key_value_pairs
        except Exception as e:
            logger.error("Error getting prompt", {
                "error": str(e),
            })
            raise e
    
    async def delete(self, key):
        key = self.key+":"+key
        return await self.db.delete_without_tx(table=self.table, where_clause=(Config.key==key))
 