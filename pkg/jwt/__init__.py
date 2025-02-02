import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta

class JWTManager:
    _instance = None
    SECRET_KEY = ""
    ALGORITHM = "HS256"

    @classmethod
    def create_jwt_token(self, data: dict, expires_delta: timedelta = None):
        """
        Create a JWT token with the given data and expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(days=7)  # Default expiration time
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def validate_jwt_token(self, token: str):
        """
        Validate a JWT token and return the decoded payload if valid.
        """
        try:
            # Decode and verify the token
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            # Handle expired token
            raise Exception("Token has expired")
        except InvalidTokenError:
            # Handle invalid token
            raise Exception("Invalid token")
    
    @classmethod
    def configure(cls, secret_key: str):
        if cls._instance is None:
            cls._instance = super(JWTManager, cls).__new__(cls)
        cls.SECRET_KEY = secret_key
        return cls._instance
        