from fastapi import WebSocket, WebSocketDisconnect
from pkg.history import MessageHistory
from typing import Dict
from app.ucase.qna import (
    logger, 
    llm_platform,
    prompt_repo,
    setup_repo,
    ws_manager,
    router,
    redis
)
import json

connected_clients: Dict[str, WebSocket] = {}  

@router.websocket("/chat/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket)
    connected_clients[client_id] = websocket  
   
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            x_session = client_id+":"+websocket.headers.get("x-session")  
            history = MessageHistory(session=x_session).redis(redis.str_conn())
            history_msg = await history.aget_messages()
            # validate model name
            if payload['llm'] is None:
                try:
                    payload['llm'] = await setup_repo.get(setup_repo.list_key()['llm']['llm'])
                except Exception:
                    payload['llm'] = "mistral"
                    
            
            if payload['model'] is None:
                try:
                    payload['model'] = setup_repo.get(setup_repo.list_key()['llm']['model'])
                except Exception:
                    payload['model'] = ""
            
            llm = llm_platform.initiate(payload['llm'], model=payload['model'])

            #  setup 
            try:
                top_k = await setup_repo.get(setup_repo.list_key()['retriever']['top_k'])
            except Exception:
                top_k = 3
            
            try:
                fetch_k = await setup_repo.get(setup_repo.list_key()['retriever']['fetch_k'])
            except Exception:
                fetch_k = 10
            
            collection = payload['collection']
            if collection is None:
                collection = await setup_repo.get(setup_repo.list_key()['retriever']['collection'])
                if collection is None:
                    await ws_manager.broadcast(f"Please setup collection or set from payload")
            

            retriever = llm.retriever(
                top_k=top_k,
                fetch_k=fetch_k,
                collection=collection
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
                resultAI = await chain_with_history.ainvoke({"input": payload['chat'], "history": history_msg}, config=config)
            except Exception as e:
                logger.error("Invok message error", {
                    "error": str(e)
                })
            logger.info("AI Result", {
                "payload": payload,
                "content": resultAI['answer'],
            })

            await connected_clients[client_id].send_text(resultAI['answer'])
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await connected_clients[client_id].send_text("A user disconnected")