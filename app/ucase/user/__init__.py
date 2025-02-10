from app.repositories.user import UserRepositories
from fastapi import APIRouter
from app.ucase import BearerAuthentication

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:user")

auth = BearerAuthentication()
router = APIRouter()
user_repo = UserRepositories()