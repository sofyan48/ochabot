from fastapi import APIRouter
from app.ucase import BasicAuth
from app.library.wrapper import AIWrapperLLM
from app.repositories import prompt, setup
from app.repositories import alchemy
from app import (
                redis,
                logger
            )

auth = BasicAuth()
router = APIRouter()
prompt_repo = prompt.Prompt()
setup_repo = setup.SetupConfig()
llm_platform = AIWrapperLLM()


from app.appctx.websocket import WebSocketManager
ws_manager = WebSocketManager()