from app.repositories import redis, logger

class SetupConfig(object):
    def __init__(self):
        self.redis = redis
        self.key = "config:"

    async def platform(self, value):
        key = self.key+"llm:platform"
        return await self.redis.set(key, value)   
    
    async def model(self, value):
        key = self.key+"llm:model"
        return await self.redis.set(key, value)   
    
    async def top_k(self, value):
        key = self.key+"retriever:top_k"
        return await self.redis.set(key, value)
    
    async def fetch_k(self, value):
        key = self.key+"retriever:fetch_k"
        return await self.redis.set(key, value)
    
    async def collection(self, value):
        key = self.key+"retriever:collection"
        return await self.redis.set(key, value)
    
    async def vector_db(self, value):
        key = self.key+"retriever:vector_db"
        return await self.redis.set(key, value)
    
    async def list_key(self):
        return {
            "retriver": {
                "top_k": "retriever:top_k",
                "fetch_k": "retriever:fetch_k",
                "collection": "retriever:collection",
                "vector_db": "retriever:vector_db",
            },
            "llm": {
                "platform": "llm:platform",
                "model": "llm:model",
            }
        }
    
    async def get(self, key):
        key = self.key+":"+key
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error("Error getting prompt", {
                "error": str(e),
            })
            raise e
    
    async def delete(self, key):
        key = self.key+":"+key
        return await self.redis.delete(self.key)
 