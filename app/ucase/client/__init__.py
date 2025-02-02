from app.repositories.socket_client import ClientSocketRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app import logger

auth = BearerAuthentication()
router = APIRouter()
client_socket_repo = ClientSocketRepositories()