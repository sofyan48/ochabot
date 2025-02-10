from pkg.jwt import JWTManager
from app.repositories.user import UserRepositories
from app.repositories.client import ClientRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:login")

auth = BearerAuthentication()
router = APIRouter()
user_repo = UserRepositories()
client_repo = ClientRepositories()
jwt = JWTManager