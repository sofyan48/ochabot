from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IGetResponseBase, response
from app.ucase.user import router, auth, logger, user_repo
from app.ucase import BasicAuth
from typing import Optional


@router.get("/users", tags=["user"])
async def list_client_socket(
        limit: Optional[int] = Query(None, description="Limit"),
        page: Optional[int] = Query(None, description="page"),
        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
    ) -> IGetResponseBase:

    auth.authenticate(credentials)
    try:
        result = await user_repo.list(limit=limit, page=page)
    except Exception as e:
        logger.error("Error list user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="User list successfully",
        data=result
    )
    