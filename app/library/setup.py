from app.repositories import redis
from app.repositories.setup import SetupConfig
from pkg.redis import Redis
from app.library import setup_repo

class SetupConfigLibrary(object):
    _instance = None  # Class variable to hold the singleton instance
    _instance_redis: Redis = None
    _instance_repo: SetupConfig = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SetupConfigLibrary, cls).__new__(cls)
            cls._instance_redis = redis
            cls._instance_repo = setup_repo
        return cls._instance
    
    @classmethod
    async def save_all(cls):
        data_config = await cls._instance_repo.list_key()
        for i in data_config:
            await cls._instance_redis.set(i.get('keys'), i.get('value'))
    
    @classmethod
    async def get_all_config(cls):
        key = "config:*"
        try:
            keys = await cls._instance_redis.keys(key=key)
            key_value_pairs = {key: await cls._instance_redis.get(key) for key in keys}
            return key_value_pairs
        except Exception as e:
            raise e
