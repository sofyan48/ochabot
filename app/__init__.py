import os 
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    WebSocket
)
from bootstrap.database import (
    register_alchemy_async,
    register_alchemy
)
from bootstrap import (
    redis,
    logging,
     openai, 
     mistral, 
     chroma,
     groq
)
from starlette.middleware.cors import CORSMiddleware

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
UPLOAD_MODEL_DIR = APP_ROOT+"/knowledge/model"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.register_redis()
    mistral.register_mistral()
    openai.register_openai()
    groq.register_groq()
    yield

# Core Application Instance
app = FastAPI(
    title="Ochabot API",
    description="This is the API documentation for Ochabot API",
    version=os.getenv("APP_VERSION", "1.0.0"),
    lifespan=lifespan
)

###### bootstaping ######
# chroma
chromadb = chroma.register_chroma_retriever()

# redis
# redis_conn = redis.register_redis()

# DB
# database
alchemy = register_alchemy_async()

# logger
logger = logging.setup_logger()


# Set all CORS origins enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup health
@app.get("/in/health")
async def root():
    return {
        "message": "health"
    }

# Add Routers
from app.router.http import routerV1
app.include_router(router=routerV1, prefix="/ex")