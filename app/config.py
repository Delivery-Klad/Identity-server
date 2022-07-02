from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    secret: str = None

    class Config:
        env_file = ".env"
