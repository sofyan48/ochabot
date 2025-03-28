from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.user import router, auth, logger, user_repo
from datetime import datetime
from pkg import utils

@router.post("/users", tags=["user"], operation_id="upsert_user") 
async def upsert_user(
        payload: request.RequestUsers,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:

    try:
        entity_user = {
            "name": payload.name,
            "email": payload.email,
            "username": payload.username,
            "password": utils.generate_hashed_password(payload.password), 
            "is_active": payload.is_active,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        if payload.id is not None:
            entity_user['id'] = payload.id
          
        last_id = await user_repo.upsert(data=entity_user)
        entity_user['id'] = last_id
    except Exception as e:
        logger.error("Error saving user", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="User saved successfully",
        data=entity_user
    )
    