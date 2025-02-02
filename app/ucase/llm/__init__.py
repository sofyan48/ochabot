from fastapi import APIRouter, Depends
from app.ucase import BearerAuthentication

auth = BearerAuthentication()
router = APIRouter()