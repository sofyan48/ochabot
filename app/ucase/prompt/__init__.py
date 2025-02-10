from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app.repositories import prompt

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:chat")

auth = BearerAuthentication()
router = APIRouter()
repoPrompt = prompt.PromptRepositories()