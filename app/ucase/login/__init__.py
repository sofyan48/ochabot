from pkg.jwt import JWTManager
from app.repositories.user import UserRepositories
from app.repositories.client import ClientRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app import logger

auth = BearerAuthentication()
router = APIRouter()
user_repo = UserRepositories()
client_repo = ClientRepositories()
jwt = JWTManager