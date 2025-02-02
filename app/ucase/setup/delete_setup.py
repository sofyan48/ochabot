from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IGetResponseBase, response
from app.ucase.setup import (
    router, 
    auth, 
    logger, 
    setup_repo
)
from app.ucase import BasicAuth

@router.delete("/setup/delete", tags=["setup"], operation_id="setup_delete") 
async def setup_llm_delete(
        key: str = Query(..., description="Key of the setup to delete"),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    try:
        await setup_repo.delete(key=key)
    except Exception as e:
        logger.error("Error saving llm config", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response(
        message="Setup deleted",
        data={}
    )