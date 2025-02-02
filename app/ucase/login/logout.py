from app.presentation import request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response


from app.ucase.login import router, logger, jwt, auth

@router.post("/logout", tags=["login"], operation_id="logout_with_password") 
async def logout_with_password(
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)
    ) -> IGetResponseBase:

    try:
        jwt.destroy_token(token=authorization.get('token'))
    except Exception as e:
        logger.error(f"Error invalidating token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not log out")

    return response(
        message="Successfully logged out", 
        data={}
    )