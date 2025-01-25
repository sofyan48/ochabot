# from fastapi import APIRouter
from fastapi import APIRouter

routerV1 = APIRouter(prefix="/v1")


from app.ucase.qna import chat, delete, history
routerV1.include_router(chat.router)
routerV1.include_router(delete.router)
routerV1.include_router(history.router)

from app.ucase.qna import socket
routerV1.include_router(socket.router)


from app.ucase.retriever import retriever
routerV1.include_router(retriever.router)

from app.ucase.llm import llm
routerV1.include_router(llm.router)


from app.ucase.prompt import (
    prompt_insert, 
    prompt_list,
    prompt_delete
)
routerV1.include_router(prompt_insert.router)
routerV1.include_router(prompt_list.router)
routerV1.include_router(prompt_delete.router)

from app.ucase.setup import(
    llm_setup,
    retrieval_setup,
    delete_setup,
    list_setup,
    get_setup
)
routerV1.include_router(llm_setup.router)
routerV1.include_router(retrieval_setup.router)
routerV1.include_router(delete_setup.router)
routerV1.include_router(list_setup.router)
routerV1.include_router(get_setup.router)