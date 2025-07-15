from typing import List, Union, Any
from pydantic import AnyHttpUrl, validator
import secrets
import os

# For Pydantic v1 compatibility
try:
    from pydantic import BaseSettings
except ImportError:
    from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Gmail Automation Dashboard"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./gmail_dashboard.db"  # Backward compatibility

    # Database Type Selection (sqlite or mysql)
    DB_TYPE: str = "sqlite"

    # MySQL Configuration from Environment Variables
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "gmail_automation"

    # SQLite Configuration
    SQLITE_DATABASE_PATH: str = "./data/gmail_dashboard.db"

    # MySQL Configuration (Alternative naming for backward compatibility)
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "gmail_automation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use DB_* variables to populate MYSQL_* variables if they exist
        if self.DB_USER:
            self.MYSQL_USER = self.DB_USER
        if self.DB_PASS:
            self.MYSQL_PASSWORD = self.DB_PASS
        if self.DB_HOST:
            self.MYSQL_HOST = self.DB_HOST
        if self.DB_PORT:
            self.MYSQL_PORT = int(self.DB_PORT)
        if self.DB_NAME:
            self.MYSQL_DATABASE = self.DB_NAME

    MYSQL_DATABASE: str = "gmail_automation"

    # Database Pool Configuration
    DB_POOL_SIZE: int = 10  # Reduced for simpler deployment
    DB_MAX_OVERFLOW: int = 20  # Reduced for simpler deployment
    DB_POOL_TIMEOUT: int = 30  # Seconds to wait for connection
    DB_POOL_RECYCLE: int = 3600  # Recycle connections after 1 hour
    DB_KEEP_ALIVE_INTERVAL: int = 1800  # Keep-alive ping every 30 minutes
    DB_ECHO: bool = False  # Set to True for SQL query logging

    # Frontend URL for email links
    FRONTEND_URL: str = "http://localhost:5173"

    # Gmail API
    GMAIL_CLIENT_ID: str = ""
    GMAIL_CLIENT_SECRET: str = ""
    GMAIL_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/gmail/callback"

    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
