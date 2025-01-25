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
    llm_platform,
    prompt_repo,
    setup_repo
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
        try:
            payload.llm = await setup_repo.get(setup_repo.list_key()['llm']['llm'])
        except Exception:
            payload.llm = "mistral"
    
    if payload.model is None:
        try:
            payload.model = await setup_repo.get(setup_repo.list_key()['llm']['model'])
        except Exception:
            payload.model = None
    payload.model = None
    
    llm = llm_platform.initiate(payload.llm, model=payload.model)
    
    #  setup 
    try: 
        top_k = await setup_repo.get(setup_repo.list_key()['retriever']['top_k'])
    except:
        top_k = 3

    try:
        fetch_k = await setup_repo.get(setup_repo.list_key()['retriever']['fetch_k'])
    except Exception:
        fetch_k = 10
    
    collection = payload.collection
    if collection is None:
        collection = await setup_repo.get(setup_repo.list_key()['retriever']['collection'])
        if collection is None:
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please setup retriever collection or set from payload"
            )
    
    retriever = llm.retriever(
        top_k=top_k,
        fetch_k=fetch_k,
        collection=collection
    )
    
    try:
        prompt = await prompt_repo.get_prompt()
    except:
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