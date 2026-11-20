import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde la raíz del backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

try:
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        PROJECT_NAME: str = "Backend Consultor WWB"
        VERSION: str = "1.0.0"
        API_PREFIX: str = "/api"
        
        GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        GOOGLE_DRIVE_FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

        class Config:
            env_file = ".env"
            extra = "ignore"

except ImportError:
    class Settings:  # Fallback si no está instalado pydantic-settings
        PROJECT_NAME: str = "Backend Consultor WWB"
        VERSION: str = "1.0.0"
        API_PREFIX: str = "/api"
        
        GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        GOOGLE_DRIVE_FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
