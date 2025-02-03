from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase.client import router, auth, logger, client_repo
from datetime import datetime
from pkg import utils

@router.post("/client", tags=["client"], operation_id="upsert_client") 
async def upsert_client(
        payload: request.RequestClient,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IGetResponseBase:

    try:
        client_api_key = utils.generate_random_string(32)
        client_secret_key = utils.generate_random_string(32)
        
        entity_client = {
            "name": payload.name,
            "api_key": client_api_key,
            "secret_key": utils.generate_hashed_password(client_secret_key), 
            "is_active": payload.is_active,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        if payload.id is not None:
            entity_client['id'] = payload.id

        last_id = await client_repo.upsert(data=entity_client)
        entity_client['id'] = last_id
    except Exception as e:
        logger.error("Error saving client", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    entity_client['secret_key'] = client_secret_key
    entity_client['api_key'] = client_api_key
    
    return response(
        message="User saved successfully",
        data=entity_client
    )
    