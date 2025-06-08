from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    togetherai_api_key: str = Field(..., env="TOGETHERAI_API_KEY")
    model_name: str = Field("lgai/exaone-3-5-32b-instruct", env="MODEL_NAME")
    temperature: float = Field(0.0, env="TEMPERATURE")

    class Config:
        env_file = ".env"

