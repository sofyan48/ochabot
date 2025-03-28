from app.presentation import request
from fastapi import HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.login import router, logger, user_repo, jwt
from datetime import datetime, timedelta
from pkg import utils

@router.post("/login", tags=["login"], operation_id="login_with_password") 
async def login_with_password(
        payload: request.RequestLogin,
    ) -> IResponseBase:
    try:
        user_data = await user_repo.get_by_username_or_email(username=payload.username)
    except Exception as e:
        logger.error("Error login user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error"
        )
    
    if not utils.verify_password(payload.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/username and password wrong"
        )
    
    expire = timedelta(days=7)
    try:
        token = jwt.create_jwt_token(data={
                "username": user_data.username,
                "roles": "user",
            },
            expires_delta=expire
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT Token not created"
        )
    # to unix time
    current_time = datetime.now()
    future_time = current_time + expire
    return response(
        message="User login successfully",
        data={
            "token": token,
            "expire": int(future_time.timestamp())
        }
    )
    