from fastapi import APIRouter, Request, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import (
    qa_retrieval, 
    chain, 
    live_chat_client
)
# import httpx

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(request: Request):
    result = await request.json()
    chats = result['payload']['body']
    conversation_id = result['payload']['conversation_id']
    
    if result['payload'].get('user') is not None:
        return {
            "message":"admin reply"
        }
    history = chain.message_history(session=conversation_id)
    history_msg = await history.aget_messages()
    history_msg_result = []
    for i in history_msg:
        history_msg_result.append({
            "content": i.content,
            "type": i.type,
        })
    resultAI = await qa_retrieval.ainvoke(chats)
    history.add_user_message(chats)
    history.add_ai_message(resultAI['result'])

    await live_chat_client.send_conversation(conversation_id,resultAI['result'])
    return response(
        message="Success",
        data={
            "query": resultAI['query'],
            "result": resultAI['result'],
        },
        meta={
            "history": history_msg_result
        }
    )
    