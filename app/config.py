from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_host_name: str = os.getenv("DATABASE_HOST_NAME")
    database_port: str = os.getenv("DATABASE_PORT")
    database_name: str = os.getenv("DATABASE_NAME")
    database_username: str = os.getenv("DATABASE_USERNAME")
    database_password: str = os.getenv("DATABASE_PASSWORD")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expires_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


settings = Settings()
