from fastapi import APIRouter
from app.ucase import BasicAuth
from app import logger
from app.repositories import prompt

auth = BasicAuth()
router = APIRouter()
repoPrompt = prompt.PromptRepositories()