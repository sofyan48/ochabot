from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from pkg.history import MessageHistory
from pkg.chain.prompter import PromptTemplate
from app.ucase.chat import (
    router, 
    auth, 
    logger, 
    llm_platform,
    prompt_repo,
    setup_repo,
    alchemy
)

@router.post("/chat", tags=["chat"], operation_id="send_chat") 
async def send_chat(
        payload: request.RequesChat, 
        x_session: str = Depends(session_middleware),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)    
    ) -> IResponseBase:
    
    history = MessageHistory(alchemy, x_session).sql()
    await history.aclear()
    history_msg = await history.aget_messages()
    setup = await setup_repo.get_all_setup()
    
    # validate model name
    if payload.llm is None:
        try:
            payload.llm = setup.get('config:llm:platform')
        except Exception:
            payload.llm = "mistral"
    
    
    if payload.model is None:
        try:
            payload.model = setup.get('config:llm:model')
        except Exception:
            payload.model = None
    
    payload.model = None
    
    llm = llm_platform.initiate(payload.llm, model=payload.model)
    try: 
        top_k = int(setup.get('config:retriever:top_k'))
    except:
        top_k = 3

    try:
        fetch_k = int(setup.get('config:retriever:fetch_k'))
    except Exception:
        fetch_k = 10
    
    collection = payload.collection
    if collection is None:
        collection = setup.get('config:retriever:collection')
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please setup retriever collection or set from payload"
            )
    try:
        vectorDB = int(setup.get('config:retriever:vector_db'))
    except Exception:
        vectorDB = "chroma"
    
    try:
        retriever = llm.retriever(
            vector=vectorDB,
            top_k=top_k,
            fetch_k=fetch_k,
            collection=collection
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Create retriever error"
        )
   
    prompt = ""
    try:
        prompt_tpl = await prompt_repo.get_prompt()
        if prompt_tpl != "":
            input_variabel = payload.input_variabels
            if input_variabel is None:
                input_variabel = ["question", "history", "context"]
            prompt = PromptTemplate(input_variables=input_variabel,template=prompt_tpl)
    except:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Prompt template or input variabel error"
            )
    
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
        logger.error("Invoke message error", {
            "error": str(e)
        })
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invoking message error",
            )
    
    logger.info("AI Result", {
        "payload": payload.model_dump(),
        "content": resultAI,
    })

    return response(
        message="Successfully",
        data={
            "result": resultAI['answer'],
        },
    )