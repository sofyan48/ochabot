from app.repositories.user import UserRepositories
from fastapi import APIRouter
from app.ucase import BasicAuth
from app import logger

auth = BasicAuth()
router = APIRouter()
user_repo = UserRepositories()