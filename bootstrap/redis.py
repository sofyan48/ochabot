# from pkg import redis
import os

# async def redis_conn():
#     return await redis.get_redis_connection(
#         host=os.getenv("REDIS_HOST", "localhost"),
#         port=os.getenv("REDIS_PORT", "6379"),
#         db=1
#     )
def str_conn():
    str_conn = "redis://{}:{}/{}".format(
        os.getenv("REDIS_HOST", "localhost"),
        os.getenv("REDIS_PORT", "6479"),
        1
    )
    return str_conn
    