from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status,  Depends, Query
from typing import Optional
from app.appctx import IResponseBase, response
from app.ucase.scope import router, auth, logger, repo

@router.get("/scope", tags=["scope"], operation_id="list_scope_prompt") 
async def list_scope_prompt(authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
            limit: Optional[int] = Query(10, description="Limit"),
            page: Optional[int] = Query(1, description="page")) -> IResponseBase:
    try:
        scope_data = await repo.list(page=page, per_page=limit)
    except Exception as e:
        logger.error("Error getting scope prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully",
        data=scope_data['data'],
        meta=scope_data['pagination'] if 'pagination' in scope_data else None,
    )