from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    SERVER_URL: str
    TOKEN_DIR: str
    HOSTS_PATH: str
    POLICY_PATH: str
    LOCAL_OVERRIDE_PATH: str

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
