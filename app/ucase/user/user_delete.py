from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Path
from app.appctx import IResponseBase, response
from app.ucase.user import router, auth, logger, user_repo


@router.delete("/users/{id}", tags=["user"], operation_id="delete_user")
async def delete_user(id: int,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:
    
    try:
        await user_repo.delete(id=id)
    except Exception as e:
        logger.error("Error detail user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="User delete successfully",
        data={}
    )
    