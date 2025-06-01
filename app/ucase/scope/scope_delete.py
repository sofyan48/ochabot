from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status,  Depends, Query
from typing import Optional
from app.appctx import IResponseBase, response
from app.ucase.scope import router, auth, logger, repo

@router.delete("/scope", tags=["scope"], operation_id="delete_scope_prompt") 
async def delete_scope_prompt(authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
            scope_id: Optional[int] = Query(None, description="The prompt id to be retrieved")
        ) -> IResponseBase:
    try:
        await repo.delete(scope_id)
    except Exception as e:
        logger.error("Error getting scope prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully",
    )