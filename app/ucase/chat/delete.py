from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from pkg.history import MessageHistory
from app.ucase.chat import router, auth, redis, logger

@router.delete("/chat",tags=["chat"], operation_id="delete_session") 
async def delete_chat_session(
        x_session: str = Depends(session_middleware),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)
    ) -> IResponseBase:
    try:
        history = MessageHistory(session=x_session).redis(redis.str_conn())
        await history.aclear()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal failure",
        )
    return response(
        message="Delete Session",
        data={
            "session": x_session,
        },
    )
