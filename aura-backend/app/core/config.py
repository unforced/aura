from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from functools import lru_cache
from dotenv import load_dotenv

# Determine the project root directory and .env path
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, ".env")

# Manually load the .env file into the environment
load_dotenv(dotenv_path=ENV_FILE_PATH)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aura"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Neo4j settings
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # ChromaDB settings
    CHROMA_HOST: str
    CHROMA_PORT: int

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    # Testing flag
    TESTING: bool = False

    # Pydantic will automatically pick up the loaded environment variables
    model_config = SettingsConfigDict(extra='ignore')

    # Path for uploaded documents
    UPLOADS_DIR: str = os.path.join(PROJECT_ROOT_DIR, "uploads")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 