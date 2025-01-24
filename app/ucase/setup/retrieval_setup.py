from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase.setup import router, auth, logger, setup_repo
from app.ucase import BasicAuth

@router.post("/setup/llm", tags=["setup"], operation_id="setup_llm_insert") 
async def setup_llm_insert(payload: request.RequestRetrievalSetup,
                        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
                    ) -> IGetResponseBase:
    auth.authenticate(credentials)
    try:
        await setup_repo.vector_db(payload.vector_db)
        await setup_repo.collection(payload.collection)
        await setup_repo.fetch_k(payload.fetch_k)
        await setup_repo.top_k(payload.top_k)
    except Exception as e:
        logger.error("Error saving retrieval", {
            "error": str(e),
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response(
        message="Retrieval config saved successfully",
        data=payload.model_dump()
    )
    