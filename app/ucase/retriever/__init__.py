from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app import (
                redis,
                logger,
                UPLOAD_MODEL_DIR
            )
from pkg.vectorstore.chromadb import ChromaDB
from app.repositories import setup


auth = BearerAuthentication()
router = APIRouter()
setup_repo = setup.SetupConfig()
chromadb = ChromaDB()
