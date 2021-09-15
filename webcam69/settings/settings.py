from pydantic import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    EXTERNAL_BILLING_API_URL: str = Field(..., env='EXTERNAL_BILLING_API_URL')
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: str = Field(..., env="REDIS_PORT")
    SELF_HOST: str = Field(..., env='SELF_HOST')
    CHECK_PAYMENT_SECONDS: int = Field(..., env='CHECK_PAYMENT_SECONDS')
    DSN: str = Field(..., env='DSN')

    class Config:
        env_file = Path(__file__).parents[1].joinpath(".env")
        env_file_encoding = 'utf-8'
