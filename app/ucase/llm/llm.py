from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from app.appctx import IResponseBase, response
from app.ucase.llm import router, auth

@router.get("/llm", tags=["llm"], operation_id="llm_list") 
async def llm_list(authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IResponseBase:
    return response(
        message="Successfully",
        data=[
            "openai",
            "mistral",
            "groq",
            "deepseek"
        ],
    )