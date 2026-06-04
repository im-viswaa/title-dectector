from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AI_API_KEY: str = ""
    AI_API_URL: str = "https://api.anthropic.com/v1/messages"
    AI_MODEL: str = "anthropic.claude-sonnet-4-5-20250929-v1:0"
    CORS_ORIGIN: str = "http://localhost:5173"
    AI_TIMEOUT_SECONDS: int = 30

    # Auth
    JWT_SECRET: str = "change-me-to-a-long-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
