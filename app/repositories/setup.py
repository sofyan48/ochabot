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

    async def upsert(self, data: Config):
        try:
            entity = {
                "key": data.key,
                "value": data.value,
                "is_active": data.is_active,
                "created_at": data.created_at,
            }
            if data.id:
                entity["id"] = data.id
                entity["updated_at"] = data.updated_at
            return await self.db.upsert_without_tx(self.model_class, entity, conflict_key=["id", "key"])
        except Exception as e:
            logger.error("Error upserting config", {
                "error": str(e),
                "data": data.model_dump() if hasattr(data, "model_dump") else str(data)
            })
            raise e

    async def list_key(self):
        try:
            query = select(Config.__table__).where(Config.is_active == True)
            result = await self.db.find(query=query, arguments={})
            return result
        except Exception as e:
            logger.error("Error listing keys", {"error": str(e)})
            raise e

    async def platform(self, value):
        try:
            key = self.key + "llm:platform"
            return await self.db.upsert_without_tx(self.model_class, {
                "key": key,
                "value": value,
                "is_active": True
            }, conflict_key=["key"])
        except Exception as e:
            logger.error("Error setting platform", {"error": str(e)})
            raise e

    async def model(self, value):
        try:
            key = self.key + "llm:model"
            return await self.db.upsert_without_tx(self.model_class, {
                "key": key,
                "value": value,
                "is_active": True
            }, conflict_key=["key"])
        except Exception as e:
            logger.error("Error setting model", {"error": str(e)})
            raise e

    async def top_k(self, value):
        try:
            key = self.key + "retriever:top_k"
            return await self.db.upsert_without_tx(self.model_class, {
                "key": key,
                "value": value,
                "is_active": True
            }, conflict_key=["key"])
        except Exception as e:
            logger.error("Error setting top_k", {"error": str(e)})
            raise e

    async def fetch_k(self, value):
        try:
            key = self.key + "retriever:fetch_k"
            return await self.db.upsert_without_tx(self.model_class, {
                "key": key,
                "value": value,
                "is_active": True
            }, conflict_key=["key"])
        except Exception as e:
            logger.error("Error setting fetch_k", {"error": str(e)})
            raise e

    async def vector_db(self, value):
        try:
            key = self.key + "retriever:vector_db"
            return await self.db.upsert_without_tx(self.model_class, {
                "key": key,
                "value": value,
                "is_active": True
            }, conflict_key=["key"])
        except Exception as e:
            logger.error("Error setting vector_db", {"error": str(e)})
            raise e

    async def fetch(self, key):
        try:
            query = select(self.table).where(Config.key == key)
            return await self.db.fetch(query=query, arguments={})
        except Exception as e:
            logger.error("Error fetching key", {"error": str(e), "key": key})
            raise e

    async def get_all_setup(self):
        try:
            key = self.key + "*"
            keys = await self.redis.keys(key)
            key_value_pairs = {key: await self.redis.get(key) for key in keys}
            return key_value_pairs
        except Exception as e:
            logger.error("Error getting all setup", {"error": str(e)})
            raise e

    async def delete(self, key):
        try:
            key = self.key + ":" + key
            return await self.db.delete_without_tx(table=self.table, where_clause=(Config.key == key))
        except Exception as e:
            logger.error("Error deleting key", {"error": str(e), "key": key})
            raise e
