from fastapi import APIRouter, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import (
                mistral, 
                chain, 
                retriever_chroma,
                redis
            )
from fastapi.security import HTTPBasicCredentials
from app.ucase import session_middleware, BasicAuth
from langchain_core.runnables.history import RunnableWithMessageHistory
from pkg.history import MessageHistory


router = APIRouter()

@router.post("/chat") 
async def send_chat(payload: request.RequesChat, 
                    x_session: str = Depends(session_middleware),
                    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    # history = MessageHistory(client=alchemy, session=x_session).sql()
    conn = redis.str_conn()
    history = MessageHistory(session=x_session).redis(conn)
    history_msg = await history.aget_messages()
    history_msg_result = []
    for i in history_msg:
        history_msg_result.append({
            "content": i.content,
            "type": i.type,
        })
    retriever = retriever_chroma.retriever(
        topK=10,
        fecthK=100,
        collection=payload.collection
    )
    qa_retrieval = chain.retrievalWithMistral("", mistral, retriever=retriever)
    chain_with_history = RunnableWithMessageHistory(qa_retrieval,
        lambda session_id: MessageHistory(session=session_id).redis(conn),
        input_messages_key="input",
        history_messages_key="message",
        output_messages_key="answer",
    )
    config = {"configurable": {"session_id": f'{x_session}'}}
    resultAI = await chain_with_history.ainvoke({"input": payload.chat, "history": history_msg}, config=config)
    return response(
        data={
            "result": resultAI['answer'],
        },
        meta={
            "history": history_msg_result
        }
    )

@router.delete("/chat")
async def clear_chat(x_session: str = Depends(session_middleware), credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    # history = MessageHistory(client=alchemy, session=x_session).sql()
    history = MessageHistory(session=x_session).redis(redis.str_conn())
    await history.aclear()
    return response(
        message="Deleted",
        data={
            "session": x_session
        }
    )