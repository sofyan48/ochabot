from fastapi import APIRouter
from app.ucase import BasicAuth
from app.library.wrapper import AIWrapperLLM
from app import (
                redis,
                logger,
                UPLOAD_MODEL_DIR
            )
from pkg.chromadb import ChromaDB
from app.repositories import setup


auth = BasicAuth()
router = APIRouter()
setup_repo = setup.SetupConfig()
chromadb = ChromaDB()
