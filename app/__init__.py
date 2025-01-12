import os 
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from bootstrap.database import (
    register_mysql,
    register_alchemy_async
)
from bootstrap import (
    redis,
    langchain,
    logging
)

from app.core import settings
from starlette.middleware.cors import CORSMiddleware

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
UPLOAD_MODEL_DIR = APP_ROOT+"/knowledge/model"

# Core Application Instance
app = FastAPI()

###### bootstaping ######
mysql = register_mysql(app)
alchemy = register_alchemy_async()
retriever_chroma = langchain.register_chroma_retriever()
mistral = langchain.register_mistral().run(redis_url=redis.str_conn(), embedings=langchain.get_embedings())
chain = langchain.register_chain_mistral()
logger = logging.setup_logger()

# Set all CORS origins enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.environ.clear()

# Setup health
@app.get("/in/health")
async def root():
    return {
        "message": "health"
    }

# Add Routers
from app.router.http import routerV1
app.include_router(router=routerV1, prefix="/ex")