from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "EasyFit App"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb://admin:password@mongodb"  # "mongodb://admin:password@localhost:27017"
    DB_NAME: str = "workout_log"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
