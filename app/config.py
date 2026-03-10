from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gcp_raw_key: str
    default_bucket_name: str

    class Config:
        env_file = ".env"

settings = Settings()