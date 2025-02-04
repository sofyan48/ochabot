from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IGetResponseBase, response
from app.ucase.setup import (
    router, 
    auth, 
    logger, 
    setup_repo
)

@router.get("/setup", tags=["setup"], operation_id="setup_list_key") 
async def setup_list_key(
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:

    try:
        data_key = await setup_repo.list_key()
    except Exception as e:
        logger.error("Error saving llm config", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    return response(
        message="Setup list key",
        data=data_key
    )