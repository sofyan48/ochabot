from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status
from pkg.jwt import JWTManager
from pkg import utils
import os

async def session_middleware(x_session: str = Header(None)):
    if x_session is None:
       raise HTTPException(status_code=400, detail="Missing x-session header")
    return x_session


class BearerAuthentication:
    def __init__(self):
        self.security = HTTPBearer()

    async def authenticate(self, authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if utils.environment_transform() == "loc" :
            return {
                "payload": {
                    "username": "local"
                },
                "token": "xxxxxxxx"
            }
        
        if authorization is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
        
        if not authorization.credentials.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")
        
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