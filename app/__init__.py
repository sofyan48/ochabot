import os 
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI
)
from bootstrap.database import (
    register_alchemy_async
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

# Core Application Instance
app = FastAPI()

###### bootstaping ######
# database
alchemy = register_alchemy_async()

# chroma
chromadb = chroma.register_chroma_retriever()

# llm
llm_openai = openai.register_openai()
openai_direct = openai.register_openai_direct_tracking_function()
llm_mistral = mistral.register_mistral()
llm_qroq = groq.register_groq()

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