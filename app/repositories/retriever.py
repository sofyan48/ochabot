from app.repositories import redis, logger

class SetupRetriever(object):
    def __init__(self):
        self.redis = redis
        self.key = "config:retriever"

    async def top_k(self, value):
        key = self.key+":top_k"
        return await self.redis.set(key, value)
    
    async def fetch_k(self, value):
        key = self.key+":fetch_k"
        return await self.redis.set(key, value)
    
    async def collection(self, value):
        key = self.key+":collection"
        return await self.redis.set(key, value)
    
    async def vector_db(self, value):
        key = self.key+":vector_db"
        return await self.redis.set(key, value)
    
    async def list_key(self):
        return [
            "top_k",
            "fetch_k",
            "collection",
            "vector_db",
        ]

    async def get(self, key: str):
        key = self.key+":"+key
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error("Error getting prompt", {
                "error": str(e),
            })
            raise e
    
    async def delete(self, key: str):
        key = self.key+":"+key
        return await self.redis.delete(self.key)
    