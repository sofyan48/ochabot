from fastapi.security import HTTPAuthorizationCredentials
from app.appctx import IGetResponseBase, response
from app.ucase.llm import router, auth, Depends

@router.get("/llm", tags=["llm"], operation_id="llm_list") 
async def llm_list(authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    return response(
        message="Successfully",
        data=[
            "openai",
            "mistral",
            "groq"
        ],
    )