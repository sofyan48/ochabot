import aioredis

# Connect to Redis
async def get_redis_connection(host, port, db):
    str_conn = "redis://{}:{}/{}".format(
        host,
        port,
        db
    )
    return await aioredis.create_redis_pool(str_conn)
