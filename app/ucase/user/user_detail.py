from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IGetResponseBase, response
from app.ucase.user import router, auth, logger, user_repo


@router.get("/users/{id}", tags=["user"], operation_id="detail_user")
async def detail_user(id: int,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IGetResponseBase:

    try:
        result = await user_repo.fetch(id=id)
    except Exception as e:
        logger.error("Error detail user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="User detail successfully",
        data=result
    )
    