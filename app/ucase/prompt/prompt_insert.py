from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.prompt import router, auth, logger, repoPrompt
from app.entity.prompt import Prompt
from datetime import datetime

@router.post("/prompt", tags=["prompt"], operation_id="insert_prompt") 
async def insert_prompt(payload: request.RequestPrompt,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IResponseBase:
    try:
        template = """
        Histroy: {history}
        Context: {context}
        Question: {input}
        Helpfull answer:
        """
        payload.prompt = payload.prompt+template
        entity = Prompt(
            id=payload.id,
            prompt=payload.prompt,
            scope_id=payload.scope_id,
            is_default=payload.is_default,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await repoPrompt.upsert(prompt=entity)
    except Exception as e:
        logger.error("Error saving prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response(
        message="Prompt saved successfully",
        data=entity.to_dict()
    )
    