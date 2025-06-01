from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status,  Depends, Query
from app.appctx import IResponseBase, response
from app.ucase.prompt import router, auth, repoPrompt, logger
from typing import Optional

@router.get("/prompt", tags=["prompt"], operation_id="prompt_list") 
async def prompt_list(authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
        limit: Optional[int] = Query(10, description="Limit"),
        page: Optional[int] = Query(1, description="page"),) -> IResponseBase:
    try: 
        prompt_data = await repoPrompt.list(page=page, per_page=limit)
    except Exception as e:
        logger.error("Error getting prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully",
        data=prompt_data['data'],
        meta=prompt_data['pagination'] if 'pagination' in prompt_data else None,
    )