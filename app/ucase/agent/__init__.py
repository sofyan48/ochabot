from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app.library.wrapper import AIWrapperLLM
from app.repositories import alchemy_url
from app.repositories import setup
from app.library.agent import agent_lib

from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:agent")

auth = BearerAuthentication()
router = APIRouter()
alchemy = alchemy_url
llm_platform = AIWrapperLLM(
    llm="openai",
    model="gpt-4o-mini",
)
setup_repo = setup.SetupConfig()