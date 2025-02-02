from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
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
    

class BearerAuthentication:
    def __init__(self):
        self.security = HTTPBearer()

    async def authenticate(self, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if authorization is None:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        
        if not authorization.credentials.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization header format")
        
        # Extract the token from the header
        token = authorization.credentials.split(" ")[1]
        try:
            payload = JWTManager.validate_jwt_token(token)
            data = {
                "payload": payload,
                "token": token
            }
            return data  # Return the payload if needed for further processing
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))