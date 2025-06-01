from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.scope import router, auth, logger, repo
from app.entity.scope_prompt import ScopePrompts
from datetime import datetime

@router.post("/scope", tags=["scope"], operation_id="insert_scope_prompt") 
async def upsert_scope_prompt(payload: request.RequestScopePrompt,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:
    try:
        entity = ScopePrompts(
            id=payload.id,
            name=payload.name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        id = await repo.upsert(scope_prompt=entity)
        entity.id = id
    except Exception as e:
        logger.error("Error saving scope prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response(
        message="Scope prompt saved successfully",
        data=entity.to_dict()
    )