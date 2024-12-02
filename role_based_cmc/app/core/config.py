from pydantic.v1 import BaseSettings
import secrets
def generate_secret_key():
    return secrets.token_hex(32)
class BaseSetting(BaseSettings):
    DB_NAME: str = "anan"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    DB_HOST: str = "localhost"
    SECRET_KEY: str = generate_secret_key()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = BaseSetting()