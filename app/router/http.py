# from fastapi import APIRouter
from fastapi import APIRouter

routerV1 = APIRouter(prefix="/v1")


from app.ucase.qna import chat
routerV1.include_router(chat.router)

from app.ucase.retriever import retriever
routerV1.include_router(retriever.router)