from pkg.jwt import JWTManager
import os


def register_jwt():
    JWTManager.configure(
        secret_key=os.environ.get("JWT_SECRET_KEY")
    )