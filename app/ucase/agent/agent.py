
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from pkg.history import MessageHistory
from app.ucase.agent import (
    router, 
    auth, 
    llm_platform,
    logger,
    alchemy,
    setup_repo,
    agent_lib,
    agent
)
from pkg.chain.prompter import ChatPromptTemplate, MessagesPlaceholder
from app.presentation import request


@router.post("/agent", tags=["agent"], operation_id="agent_chat")
async def chat_with_agent(
        payload: request.RequesChatAgent,
        x_session: str = Depends(session_middleware),
        # authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
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

    if payload.llm != "openai":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"LLM platform '{payload.llm}' is not supported, for other llm platform is coming soon."
        )
    
    
    if payload.model is None:
        try:
            payload.model = setup.get('config:llm:model')
        except Exception:
            payload.model = "gpt-4o-mini"
    tools = []
    if payload.agent is None:
        tools = agent_lib.list_tools()
    else:
        try:
            tool = agent_lib.get_tool(payload.agent)
        except ValueError as e:
            logger.error("Tool not found", {
                "error": str(e),
                "agent": payload.agent
            })
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Tool '{payload.agent}' not found"
            )
        tools.append(tool)
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        ("system", "Kamu adalah agen pintar yang bisa menggunakan tools jika perlu."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])


    
    try:
        llm = llm_platform.initiate(llm=payload.llm, model=payload.model).run(model=payload.model)
        agent = agent_lib.agent_functions(llm=llm, tools=tools, model=payload.model, prompt=prompt)
        agent_executor = agent_lib.executor(agent=agent, tools=tools, verbose=False, return_intermediate_steps=True)
        result = agent_executor.invoke({"history": history_msg, "input": payload.chat})
    except Exception as e:
        logger.error("Error in agent chat", {
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Agent chat failed, please try again"
        )
    steps =result.get("intermediate_steps", [])
    return response(
        message="Successfully",
        data={
            "result": result.get("output", ""),
            "agent_executor": steps,
        }
    )