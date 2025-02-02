from app.repositories.socket_client import ClientSocketRepositories
from fastapi import APIRouter
from app.ucase import BasicAuth
from app import logger

auth = BasicAuth()
router = APIRouter()
client_socket_repo = ClientSocketRepositories()