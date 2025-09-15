from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Settings(BaseSettings):
    # Environment variables for security and authentification
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment variables for SQLAlchemy
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @property
    # def DATABASE_URL_asyncpg(self):
    #     # postgresql+psycopg://postgres:postgres@localhost:5432/sa
    #     return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # model_config = SettingConfigDict(env_file=".env")
    class Config:
        env_file = ".env"  # путь до .env
        env_file_encoding = "utf-8"
    # model_config = SettingConfigDict(env_file=".env")
# Создаём единственный экземпляр
settings = Settings()

