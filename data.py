from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    openai_api_token: str
    amplitude_api_key: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
