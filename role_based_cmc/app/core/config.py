from pydantic.v1 import BaseSettings
import secrets
def generate_secret_key():
    return secrets.token_hex(32)
class BaseSetting(BaseSettings):
    DB_NAME: str = "anan"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    DB_HOST: str = "localhost"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES :int = 30
    PUBLIC_PATHS = [
        "/",
        "/api/auth/login",
        "/api/users/register",
        "/docs",
        "/openapi.json",
    ]

settings = BaseSetting()