import os 
from contextlib import asynccontextmanager
from fastapi import FastAPI
from bootstrap.database import (
    register_alchemy_async,
)
from dotenv import load_dotenv
from bootstrap import (
    redis,
    logging,
    openai, 
    mistral, 
    groq,
    vectorstore,
    prompter,
    minio,
    jwt,
    deepseek,
    ollama,
)
from starlette.middleware.cors import CORSMiddleware

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
UPLOAD_MODEL_DIR = APP_ROOT+"/knowledge/model"

# load env
load_dotenv()

# bootstraping
register_alchemy_async()
prompter.regist_default_prompter()
minio.register_storage_minio()
jwt.register_jwt()

# vectorstores
# vectorstore.register_chroma_retriever()
vectorstore.register_elasticsearch_vectorstore()

# LLM Platform
mistral.register_mistral()
openai.register_openai()
openai.register_openai_direct()
groq.register_groq()
deepseek.register_deepseek()
ollama.register_ollama()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.register_redis()
    # initial setup
    from app.library.setup import SetupConfigLibrary
    await SetupConfigLibrary.save_all()
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