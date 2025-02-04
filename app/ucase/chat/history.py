from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from pkg.history import MessageHistory
from app.ucase.chat import router, auth, redis

@router.get("/chat", tags=["chat"], operation_id="chat_histories") 
async def chat_histories(
        x_session: str = Depends(session_middleware),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)
    ) -> IGetResponseBase:

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