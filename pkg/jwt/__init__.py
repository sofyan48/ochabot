import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
from pkg import utils

class JWTManager:
    _instance = None
    SECRET_KEY = ""
    ALGORITHM = "HS256"
    _blacklist = set() 

    @classmethod
    def create_jwt_token(cls, data: dict, expires_delta: timedelta = None):
        """
        Create a JWT token with the given data and expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(days=7)  # Default expiration time
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def destroy_token(cls, token: str):
        """
        Invalidate a JWT token by adding it to the blacklist.
        """
        cls._blacklist.add(token)
        
    @classmethod
    def validate_jwt_token(cls, token: str):
        """
        Validate a JWT token and return the decoded payload if valid.
        """
        if token in cls._blacklist:
            raise Exception("Token has been invalidated")

        if utils.environment_transform() == "loc":
            # mockup payload
            return {'username': 'local', 'roles': 'user', 'exp': 1739309149}
        
        try:
            # Decode and verify the token
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
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
        