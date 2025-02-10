from fastapi import APIRouter
from app.ucase import BearerAuthentication

auth = BearerAuthentication()
router = APIRouter()