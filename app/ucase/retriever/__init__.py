from fastapi import APIRouter
from app.ucase import BasicAuth
from app.library.wrapper import AIWrapperLLM
from app import (
                redis,
                logger,
                chromadb,
                UPLOAD_MODEL_DIR
            )

from app.repositories import setup


auth = BasicAuth()
router = APIRouter()
setup_repo = setup.SetupConfig()