from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app import (
                redis,
                UPLOAD_MODEL_DIR
            )
from pkg.vectorstore.chromadb import ChromaDB
from app.repositories import setup
from app.repositories.ingest_document import IngestDocumentRepositories
from app.repositories import setup
from app.library import vectorstoreDB


from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:ingest")


auth = BearerAuthentication()
router = APIRouter()
setup_repo = setup.SetupConfig()
chromadb = ChromaDB()
setup_repo = setup.SetupConfig()
ingest_docs_repo = IngestDocumentRepositories()


from app.library.storage import Storage
from app.library import minio
minio_client = Storage(minio)