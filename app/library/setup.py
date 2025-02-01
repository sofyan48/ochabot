from app.repositories import redis
from app.library import setup_repo


class SetupConfig(object):
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SetupConfig, cls).__new__(cls)
            cls._instance.redis = redis
            cls._instance.key = "config:"
            cls._instance.repo = setup_repo
        return cls._instance

    async def get_all_setup(self):

        key = self.key + "*"
        try:
            keys = await self.redis.keys(key)
            key_value_pairs = {key: await self.redis.get(key) for key in keys}
            return key_value_pairs
        except Exception as e:
            raise e

    async def delete(self, key):
        key = self.key + ":" + key
        return await self.db.delete_without_tx(table=self.table, where_clause=(Config.key == key))
