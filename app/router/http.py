# from fastapi import APIRouter
from fastapi import APIRouter
from app.ucase import (
    chat,
    retriever,
    datasheet,
)
routerV1 = APIRouter(prefix="/v1")
routerV1.include_router(chat.router)
routerV1.include_router(retriever.router)
routerV1.include_router(datasheet.router)