from fastapi import APIRouter
from app.ucase import BasicAuth
from app import logger
from app.repositories import setup

auth = BasicAuth()
router = APIRouter()
setup_repo = setup.SetupConfig()