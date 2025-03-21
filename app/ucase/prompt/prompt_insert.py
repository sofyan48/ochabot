from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.prompt import router, auth, logger, repoPrompt

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
        await repoPrompt.save(prompt=payload.prompt, is_default=payload.is_default)
    except Exception as e:
        logger.error("Error saving prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response(
        message="Prompt saved successfully",
        data=payload.model_dump()
    )
    