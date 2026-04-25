import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()


class Settings:
    # JWT настройки
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

    # Приложение
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Blog")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()