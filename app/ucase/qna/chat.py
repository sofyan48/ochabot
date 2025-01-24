from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from app.ucase import session_middleware, BasicAuth
from pkg.history import MessageHistory
from app.ucase.qna import (
    router, 
    auth, 
    redis, 
    logger, 
    AIWrapperLLM,
    prompt_repo
)

@router.post("/chat", tags=["chat"], operation_id="send_chat") 
async def send_chat(payload: request.RequesChat, 
                    x_session: str = Depends(session_middleware),
                    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    
    auth.authenticate(credentials=credentials)
    conn = redis.str_conn()

    history = MessageHistory(session=x_session).redis(conn)
    history_msg = await history.aget_messages()
     # validate model name
    if payload.llm is None:
        payload.llm = "mistral"
    llm = AIWrapperLLM().initiate(payload.llm, model=payload.model)
    
    retriever = llm.retriever(
        top_k=3,
        fetch_k=10,
        collection=payload.collection
    )
    
    prompt = await prompt_repo.get_prompt()
    if prompt is None:
        prompt = ""

    qa_retrieval = llm.retrieval(prompt, retriever=retriever)
    chain_with_history = llm.chain_with_history(
        qa_retrieval,
        history=history,
        input_messages_key="input",
        history_messages_key="message_store",
        output_messages_key="answer",
    )

    config = {"configurable": {"session_id": f'{x_session}'}}
    try:
        resultAI = await chain_with_history.ainvoke({"input": payload.chat, "history": history_msg}, config=config)
    except Exception as e:
        logger.error("Invok message error", {
            "error": str(e)
        })
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Internal failure",
            )
    logger.info("AI Result", {
        "payload": payload.model_dump(),
        "content": resultAI['answer'],
    })
    return response(
        message="Successfully",
        data={
            "result": resultAI['answer'],
        },
    )