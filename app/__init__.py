import os 
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    WebSocket
)
from bootstrap.database import (
    register_alchemy_async,
)
from bootstrap import (
    redis,
    logging,
     openai, 
     mistral, 
     groq,
    vectorstore
)
from starlette.middleware.cors import CORSMiddleware

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
UPLOAD_MODEL_DIR = APP_ROOT+"/knowledge/model"


register_alchemy_async()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.register_redis()
    mistral.register_mistral()
    openai.register_openai()
    groq.register_groq()
    vectorstore.register_chroma_retriever()
    yield
    # clearing env after shutdown
    os.environ.clear()

# Core Application Instance
app = FastAPI(
    title="Ochabot API",
    description="This is the API documentation for Ochabot API",
    version=os.getenv("APP_VERSION", "1.0.0"),
    lifespan=lifespan
)

# Database

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