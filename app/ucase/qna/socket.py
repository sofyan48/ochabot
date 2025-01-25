from fastapi import WebSocket, WebSocketDisconnect
from pkg.history import MessageHistory
from app.ucase.qna import (
    auth, 
    redis, 
    logger, 
    llm_platform,
    prompt_repo,
    setup_repo,
    ws_manager,
    router
)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast("A user disconnected")