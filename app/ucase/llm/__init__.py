from fastapi import APIRouter, Depends
from app.ucase import BasicAuth

auth = BasicAuth()
router = APIRouter()