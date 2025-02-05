from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.appctx import IResponseBase, response
from app.ucase.setup import router, auth, logger, setup_repo, setup_library

@router.post("/setup/retriever", tags=["setup"], operation_id="setup_retriever_insert") 
async def setup_retriever_insert(payload: request.RequestRetrievalSetup,
                        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
                    ) -> IResponseBase:
    try:
        await setup_repo.vector_db(payload.vector_db)
        await setup_repo.collection(payload.collection)
        await setup_repo.fetch_k(str(payload.fetch_k))
        await setup_repo.top_k(str(payload.top_k))
        await setup_library.save_all()
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
    