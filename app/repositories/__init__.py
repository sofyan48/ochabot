from pkg.redis import Redis
from pkg.database.alchemy import AlChemy
from app import logger

redis = Redis()
alchemy_url = AlChemy.get_write_uri()
alchemy = AlChemy
