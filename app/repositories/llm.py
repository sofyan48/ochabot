from app.repositories import redis, logger

class SetupLLM(object):
    def __init__(self):
        self.redis = redis
        self.key = "config:llm"

    async def model(self, value):
        key = self.key+":model"
        return await self.redis.set(key, value)   

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
 