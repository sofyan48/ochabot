from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status,  Depends, Query
from app.appctx import IResponseBase, response
from typing import Optional
from app.ucase.prompt import router, auth, repoPrompt, logger

@router.get("/prompt/set", tags=["prompt"], operation_id="prompt_set") 
async def prompt_set(
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
        prompt_id: Optional[int] = Query(None, description="The prompt id to be retrieved"),
        scope_id: Optional[int] = Query(None, description="The scope_id id to be retrieved"),
    ) -> IResponseBase:
    try: 
        await repoPrompt.set_prompt_config(id_prompt=prompt_id, scope_id=scope_id)
    except Exception as e:
        logger.error("Error getting prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully",
        data={
            "prompt": prompt_id
        },
    )