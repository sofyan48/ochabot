from fastapi.security import HTTPBasicCredentials
from app.ucase import session_middleware, BasicAuth
from app.appctx import IGetResponseBase, response
from app.ucase.llm import router, auth, Depends

@router.get("/llm", tags=["llm"], operation_id="llm_list") 
async def llm_list(credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    auth.authenticate(credentials=credentials)
    return response(
        message="Successfully",
        data=[
            "openai",
            "mistral",
            "groq"
        ],
    )