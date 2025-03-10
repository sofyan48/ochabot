from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IResponseBase, response
from app.ucase.user import router, auth, logger, user_repo

from typing import Optional


@router.get("/users", tags=["user"])
async def list_client_socket(
        limit: Optional[int] = Query(10, description="Limit"),
        page: Optional[int] = Query(1, description="page"),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:
    try:
        result = await user_repo.list(limit=limit, page=page)
    except Exception as e:
        logger.error("Error list user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    filtered_result = []
    for user in result:
        user_data = user.copy()
        user_data.pop('password', None)
        filtered_result.append(user_data)
    return response(
        message="User list successfully",
        data=filtered_result
    )
    