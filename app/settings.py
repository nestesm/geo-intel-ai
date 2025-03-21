from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
from typing import Literal
from pydantic import EmailStr, Field, field_validator


class Settings(BaseSettings):

    ENVIRONMENT: Literal['dev', 'prod'] = 'dev'

    DATABASE_HOST: str  
    DATABASE_PORT: str 
    DATABASE_USER: str
    DATABASE_PASSWORD: str 
    DATABASE_NAME: str 

    SECRET_JWT: str = Field(..., min_length=32)
    SECRET_PASS: str = Field(..., min_length=12)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST: str 
    SMTP_PORT: int = Field(..., ge=1, le=65535)
    SMTP_USER: EmailStr 
    SMTP_PASSWORD: str 

    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str 
    
    @property
    def DATABASE_URL_async(self) -> str:
        return (
            f'postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}'
            f'@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
        )
    
    @property
    def DATABASE_URL_sync(self) -> str:
        return (
            f'postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )
    
    class Config:
        env_file = find_dotenv(usecwd=True)
        case_sensitive=True

   
settings = Settings() 