import redis.asyncio as redis
from pkg.logger.logging import logger

class Redis:
    redis_client: redis.Redis = None
    @classmethod
    async def connect(
        cls, host: str = "localhost", port: int = 6379, username=None, password=None
    ) -> redis.Redis:
        try:
        # Connect to Redis server
            cls.redis_client = redis.Redis(
                host=host, 
                port=port, 
                password=password,
                decode_responses=True
            )
        except redis.RedisError as e:
            logger.error("Error connecting to Redis", {"error": str(e)})
            raise e
        await cls.redis_client

    @classmethod
    async def set(cls, key: str, value: str):
        await cls.redis_client.set(key, value)

    @classmethod
    async def get(cls, key: str):
        value = await cls.redis_client.get(key)
        return value
    
    @classmethod
    async def keys(cls, key: str):
        value = await cls.redis_client.keys(key)
        return value
    
    @classmethod
    async def getall(cls, key: str):
        value = await cls.redis_client.hgetall(key)
        return value
    
    @classmethod
    async def delete(cls, key: str):
        await cls.redis_client.delete(key)

    