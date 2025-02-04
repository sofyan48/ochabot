
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Query
from app.appctx import IGetResponseBase, response
from app.ucase.setup import (
    router, 
    auth, 
    logger, 
    setup_repo
)

@router.get("/setup/detail", tags=["setup"], operation_id="setup_detail_key") 
async def setup_detail_key(
        name: str = Query(..., description="Name of the setup"),
        config: str = Query(..., description="config of the setup"),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    try:
        key = "config:"+name+":"+config
        data_key = await setup_repo.get(key=key)
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