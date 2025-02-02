from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase.setup import router, auth, logger, setup_repo, setup_library
from app.ucase import BasicAuth

@router.post("/user", tags=["user"], operation_id="upsert") 
async def upsert(payload: request.RequestUsers,
                        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
                    ) -> IGetResponseBase:
    auth.authenticate(credentials)
    try:
       pass
    except Exception as e:
        logger.error("Error saving user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="User saved successfully",
        data=payload.model_dump()
    )
    