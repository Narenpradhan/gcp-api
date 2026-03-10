from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_application_credentials: str
    default_bucket_name: str

    class Config:
        env_file = ".env"

settings = Settings()