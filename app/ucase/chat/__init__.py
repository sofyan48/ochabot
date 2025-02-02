from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app.library.wrapper import AIWrapperLLM
from app.repositories import prompt, setup
from app.repositories import alchemy_url
from app import (
                redis,
                logger,
                UPLOAD_MODEL_DIR
            )


auth = BearerAuthentication()
router = APIRouter()
prompt_repo = prompt.PromptRepositories()
setup_repo = setup.SetupConfig()
llm_platform = AIWrapperLLM()

from pkg.vectorstore.chromadb import ChromaDB
chromadb = ChromaDB()

from app.appctx.websocket import WebSocketManager
ws_manager = WebSocketManager()
alchemy = alchemy_url

from app.library.storage import Storage
from app.library import minio
minio_client = Storage(minio)