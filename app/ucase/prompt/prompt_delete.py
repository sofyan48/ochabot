from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth
from fastapi import HTTPException, status,  Depends, Query
from typing import Optional
from app.appctx import IGetResponseBase, response
from app.ucase.prompt import router, auth, repoPrompt, logger

@router.delete("/prompt", tags=["prompt"], operation_id="prompt_delete") 
async def prompt_delete(
        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
        prompt_id: Optional[int] = Query(None, description="The prompt id to be retrieved")
    ) -> IGetResponseBase:
    auth.authenticate(credentials=credentials)
    try:
        await repoPrompt.delete(prompt_id)
        await repoPrompt.delete_prompt_config()
    except Exception as e:
        logger.error("Error getting prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully delete",
        data={},
    )