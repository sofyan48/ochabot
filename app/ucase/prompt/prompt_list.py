from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth
from fastapi import HTTPException, status,  Depends
from app.appctx import IGetResponseBase, response
from app.ucase.prompt import router, auth, repoPrompt, logger

@router.get("/prompt", tags=["prompt"], operation_id="prompt_list") 
async def prompt_list(credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    auth.authenticate(credentials=credentials)
    try: 
        prompt_data = await repoPrompt.list()
    except Exception as e:
        logger.error("Error getting prompt", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="Successfully",
        data={
            "prompt": prompt_data
        },
    )