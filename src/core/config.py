import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()