from databases import Database
from sqlalchemy.ext.declarative import declarative_base

from ..core.config import config


def get_db() -> Database:
    params = {
        'min_size': config.DB_MIN_POOL_SIZE,
        'max_size': config.DB_MAX_POOL_SIZE,
    }
    return Database(config.db_url, **params)


database = get_db()
Base = declarative_base()
metadata = Base.metadata
