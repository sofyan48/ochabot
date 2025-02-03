from app.presentation import request
from fastapi import HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase.login import router, logger, client_repo, jwt
from datetime import datetime, timedelta
from pkg import utils

@router.post("/grant", tags=["login"], operation_id="grant_client") 
async def grant_client_with_password(
        payload: request.RequestGrantClient,
    ) -> IGetResponseBase:
    try:
        client_data = await client_repo.fetch_row_by_apikey(payload.api_key)
    except Exception as e:
        logger.error("Error login user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error"
        )
    if client_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Api Key or Secret key not found"
        )
    if not utils.verify_password(payload.secret_key, client_data.secret_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Api Key or Secret Key wrong"
        )
    
    expire = timedelta(days=365)
    try:
        token = jwt.create_jwt_token(data={
                "apikey": client_data.name,
                "roles": "client",
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
        message="Client login successfully",
        data={
            "token": token,
            "expire": int(future_time.timestamp())
        }
    )
    