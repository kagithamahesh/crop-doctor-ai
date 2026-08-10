from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
     APP_NAME:str
     DATABASE_URL: str
     SECRET_KEY: str
     ALGORITHM: str
     ACCESS_TOKEN_EXPIRE_MINUTES: int
     GROQ_API_KEY: str
     GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",

        extra="ignore"
    )


settings = Settings()
