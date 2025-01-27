from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from fastapi.security import HTTPBasicCredentials
from app.ucase import session_middleware, BasicAuth
from pkg.history import MessageHistory
from app.ucase.qna import router, auth, redis

@router.get("/chat/history", tags=["chat"], operation_id="chat_histories") 
async def chat_histories(x_session: str = Depends(session_middleware),
                    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    auth.authenticate(credentials=credentials)
    try:
        history = MessageHistory(session=x_session).redis(redis.str_conn())
        data_history = await history.aget_messages()
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal failure",
        )
    return response(
        message="History Session",
        data=data_history,
    )