__all__ = ("create_web_api_app",)

from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import URL

from test_task.configs import (
    ClientAccessConfig,
    load_postgres_config,
    load_client_access_config,
)
from .routes import router


def create_web_api_app() -> FastAPI:
    app = FastAPI()

    postgres_config = load_postgres_config()
    client_access_config = load_client_access_config()

    url = URL.create(
        drivername="postgresql.psycopg",
        username=postgres_config.username,
        password=postgres_config.password,
        host=postgres_config.host,
        port=postgres_config.port,
        database=postgres_config.database,
    )
    engine = create_async_engine(url, plugins=["geoalchemy2"])
    session_maker = async_sessionmaker(engine)

    async def session_factory() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    app.dependency_overrides[AsyncSession] = session_factory
    app.dependency_overrides[ClientAccessConfig] = lambda: client_access_config

    app.include_router(router)

    return app