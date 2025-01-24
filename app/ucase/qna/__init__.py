from fastapi import APIRouter
from app.ucase import BasicAuth
from app.library.wrapper import AIWrapperLLM
from app.repositories import prompt
from app import (
                redis,
                logger
            )

auth = BasicAuth()
router = APIRouter()
prompt_repo = prompt.Prompt()