import os
from functools import lru_cache

from pydantic import BaseSettings

LOCAL = 'LOCAL'


class AppConfig(BaseSettings):
    ENV: str = os.getenv("ENVIRONMENT", LOCAL)
    SERVER_NAME: str = 'Users Manager API'
    DESCRIPTION = "API for managing users"
    VERSION: str = '0.0.1'
    DEBUG: bool = False
    API_V1_STR: str = '/v1'

    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_MIN_POOL_SIZE = os.getenv('DB_MIN_POOL_SIZE', 5)
    DB_MAX_POOL_SIZE = os.getenv('DB_MAX_POOL_SIZE', 10)

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class LocalConfig(AppConfig):
    DEBUG = True


@lru_cache()
def get_config(env: str = LOCAL) -> AppConfig:
    if env == LOCAL:
        return LocalConfig()
    raise Exception('Not supported env')


config = get_config()
