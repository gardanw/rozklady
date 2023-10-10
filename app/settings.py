from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://username:password@localhost/database_name"

    class Config:
        env_file = ".env"  # Plik .env zawierający zmienne środowiskowe


settings = Settings()
