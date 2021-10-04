from fastapi import FastAPI

from fastapi_postgresql.api.v1 import v1_router

from .core.config import config
from .db.base import database


def get_app() -> FastAPI:
    app = FastAPI(
        title=config.SERVER_NAME,
        description=config.DESCRIPTION,
        version=config.VERSION,
        debug=config.DEBUG,
    )
    app.include_router(v1_router, prefix=config.API_V1_STR, tags=['v1'])
    return app


app = get_app()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root() -> dict:
    return {"status": "happy"}
