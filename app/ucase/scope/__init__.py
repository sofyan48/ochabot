from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app.repositories import scope_prompt

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:scope")

auth = BearerAuthentication()
router = APIRouter()
repo = scope_prompt.ScopePromptRepositories()