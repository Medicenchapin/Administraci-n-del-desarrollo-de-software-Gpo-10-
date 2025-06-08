# src/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Indicamos dónde cargar el .env
    model_config = SettingsConfigDict(env_file=".env")
    togetherai_api_key: str = Field(..., env="TOGETHERAI_API_KEY")
    model_name: str          = Field("lgai/exaone-3-5-32b-instruct", env="MODEL_NAME")
    temperature: float       = Field(0.0, env="TEMPERATURE")

settings = Settings()

