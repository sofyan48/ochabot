from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from pkg.history import MessageHistory
from pkg.chain.prompter import PromptTemplate
from app.library.chaining.retrieval_qa import RetrievalQAChainLibrary
from app.library import Vectorstores
from app.ucase.chat import (
    router, 
    auth, 
    logger, 
    llm_platform,
    prompt_repo,
    setup_repo,
    alchemy,
    scope_repo
)

from pkg.openai import OpenAIDirect

@router.post("/chat", tags=["chat"], operation_id="send_chat") 
async def send_chat(
        payload: request.RequesChat, 
        x_session: str = Depends(session_middleware),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)    
    ) -> IResponseBase:
    
    history = MessageHistory(alchemy, x_session).sql()
    history_msg = await history.aget_messages()
    setup = await setup_repo.get_all_setup()
    # validate model name
    if payload.llm is None:
        try:
            payload.llm = setup.get('config:llm:platform')
        except Exception:
            payload.llm = "openai"
    
    
    if payload.model is None:
        try:
            payload.model = setup.get('config:llm:model')
        except Exception:
            payload.model = "gpt-4o-mini"
    
    try: 
        top_k = int(setup.get('config:retriever:top_k'))
    except:
        top_k = 3

    try:
        fetch_k = int(setup.get('config:retriever:fetch_k'))
    except Exception:
        fetch_k = 10
    
    collection = ""
    try:
        scope_data = await scope_repo.get(payload.scope_id)
        collection = scope_data.name
    except Exception as e:
        logger.error("Error getting scope data", {
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot get scope data"
        )
    
    try:
        vectorDB = setup.get('config:retriever:vector_db')
    except Exception:
        vectorDB = None

    prompt = ""
    try:
        prompt_tpl = await prompt_repo.get_prompt(payload.scope_id)
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

    
    try:
        retriever = Vectorstores().configure(vectorestore=vectorDB).retriever(
            topK=top_k,
            fetchK=fetch_k,
            collection=collection,
        )
    except Exception as e:
        logger.error("Create retriever error", {
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Create retriever error"
        )

    try:
        chaining = RetrievalQAChainLibrary(retriever)
        platform = llm_platform.initiate(payload.llm, model=payload.model)
        retrieval = chaining.retrieval(promp_tpl=prompt, platform=platform, model=payload.model)
        chain_with_history = chaining.chain_with_history(
            retrival=retrieval,
            history=history,
            input_messages_key="input",
            history_messages_key="message_store",
            output_messages_key="answer",
        )
    except Exception as e:
        logger.error("Chaining process error", {
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Chaining process error"
        )
    
    try:
        config = {"configurable": {"session_id": f'{x_session}'}}
        resultAI = await chain_with_history.ainvoke({"input": payload.chat, "history": history_msg}, config=config)
    except Exception as e:
        logger.error("Invoke message error", {
            "error": str(e)
        })
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invoking message error: "+str(e),
            )   
    
    return response(
        message="Successfully",
        data={
            "result": resultAI['answer'],
        }
    )