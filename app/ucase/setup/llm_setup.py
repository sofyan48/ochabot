from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase.setup import router, auth, logger, setup_repo, setup_library
from app.ucase import BasicAuth

@router.post("/setup/llm", tags=["setup"], operation_id="setup_llm_insert") 
async def setup_llm_insert(payload: request.RequestLLMSetup,
                        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
                    ) -> IGetResponseBase:
    auth.authenticate(credentials)
    try:
        await setup_repo.model(payload.model)
        await setup_repo.platform(payload.platform)
        await setup_library.save_all()
    except Exception as e:
        logger.error("Error saving llm config", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return response(
        message="LLM config saved successfully",
        data=payload.model_dump()
    )
    