# from fastapi import APIRouter
from fastapi import APIRouter

routerV1 = APIRouter(prefix="/v1")


from app.ucase.qna import chat, delete, history
routerV1.include_router(chat.router)
routerV1.include_router(delete.router)
routerV1.include_router(history.router)


from app.ucase.retriever import retriever
routerV1.include_router(retriever.router)

from app.ucase.llm import llm
routerV1.include_router(llm.router)


from app.ucase.prompt import prompt_insert
routerV1.include_router(prompt_insert.router)