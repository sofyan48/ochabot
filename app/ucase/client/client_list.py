from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IResponseBase, response
from app.ucase.client import router, auth, logger, client_repo

from typing import Optional


@router.get("/client", tags=["client"])
async def list_client(
        limit: Optional[int] = Query(10, description="Limit"),
        page: Optional[int] = Query(1, description="page"),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:
    try:
        result = await client_repo.fetch(limit=limit, page=page)
    except Exception as e:
        logger.error("Error list user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Client list successfully",
        data=result
    )
    