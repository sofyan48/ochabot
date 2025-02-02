from fastapi import Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets, os
from fastapi import HTTPException, status
from pkg.jwt import JWTManager

async def session_middleware(x_session: str = Header(None)):
    if x_session is None:
       raise HTTPException(status_code=400, detail="Missing x-session header")
    return x_session


class BasicAuth:
    def __init__(self):
        self.security = HTTPBasic()

    def authenticate(self, credentials: HTTPBasicCredentials):
        correct_username = secrets.compare_digest(credentials.username, os.getenv("APP_USERNAME"))
        correct_password = secrets.compare_digest(credentials.password, os.getenv("APP_PASSWORD"))

        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials
    
# JWT Middleware
async def jwt_middleware(x_jwt: str = Header(None)):
    if x_jwt is None:
        raise HTTPException(status_code=401, detail="Missing x-jwt header")
    try:
        payload = JWTManager.validate_jwt_token(x_jwt)
        return payload  # Return the payload if needed for further processing
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))