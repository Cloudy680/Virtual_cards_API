from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # путь до .env
        env_file_encoding = "utf-8"

# Создаём единственный экземпляр
settings = Settings()

