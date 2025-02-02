from app.repositories.user import UserRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app import logger

auth = BearerAuthentication()
router = APIRouter()
user_repo = UserRepositories()