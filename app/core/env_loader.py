from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSettings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

env = EnvSettings()