from fastapi import APIRouter
from app.ucase import BearerAuthentication
from app.repositories import setup
from app.library.setup import SetupConfigLibrary


from pkg.logger.logging import configure_logger
logger = configure_logger("ucase:setup")

auth = BearerAuthentication()
router = APIRouter()
setup_repo = setup.SetupConfig()
setup_library = SetupConfigLibrary()