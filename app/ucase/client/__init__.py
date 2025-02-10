from app.repositories.socket_client import ClientSocketRepositories
from app.repositories.client import ClientRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:chat")

auth = BearerAuthentication()
router = APIRouter()
client_socket_repo = ClientSocketRepositories()
client_repo = ClientRepositories()