from pkg.redis import Redis
from pkg.database.alchemy import AlChemy
from app import logger

redis = Redis()
alchemy_url = AlChemy.get_write_uri()

from app.repositories.socket_client import ClientSocketRepositories
client_socket_repo = ClientSocketRepositories(AlChemy)
