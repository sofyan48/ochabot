import os
from pkg import redis

def str_conn():
    str_conn = "redis://:{}@{}:{}/{}".format(
        os.getenv("REDIS_PASSWORD"),
        os.getenv("REDIS_HOST"),
        os.getenv("REDIS_PORT"),
        os.getenv("REDIS_DB")
    )
    return str_conn

async def register_redis() -> redis.Redis:
    return await redis.Redis.connect(
        os.getenv("REDIS_HOST"), 
        int(os.getenv("REDIS_PORT")), 
        os.getenv("REDIS_DB"), 
        os.getenv("REDIS_PASSWORD")
    )