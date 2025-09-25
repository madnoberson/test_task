import sys
import importlib.resources
from typing import Annotated

from cyclopts import App, Parameter
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from gunicorn.app.wsgiapp import run as run_gunicorn

import test_task.migrations
from alembic import config as alembic_config
from .configs import load_postgres_config
from .application import create_building, create_domain, create_organization


_ALEMBIC_CONFIG_PATH = str(
    importlib.resources
    .files(test_task.migrations)
    .joinpath("alembic.ini")
)


def main() -> None:
    app = App()

    app.command(alembic)
    app.command(create_fake_data)
    app.command(run_web_api)

    app()


def alembic(commands: list[str]) -> None:
    """
    Runs alembic with provided args and options.
    """
    alembic_config.main(["-c", _ALEMBIC_CONFIG_PATH, *commands])


async def create_fake_data() -> None:
    postgres_config = load_postgres_config()

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

    async with session_maker() as session:
        await create_building(
            session=session,
            id=1,
            address="ул. Пушкина, д.27, Москва, 143350",
            lat=55.609715,
            lon=37.211006,
        )
        await create_domain(
            session=session,
            id=1,
            parent_id=None,
            name="Торты",
        )
        await create_domain(
            session=session,
            id=2,
            parent_id=1,
            name="Маленькие торты",
        )
        await create_domain(
            session=session,
            id=3,
            parent_id=2,
            name="Мельчайшие торты",
        )
        await create_domain(
            session=session,
            id=4,
            parent_id=1,
            name="Большие торты",
        )
        await create_organization(
            session=session,
            id=1,
            building_id=1,
            name="КНОПКАБАБЛО",
            phone_numbers=["+79993999999", "+79893396959"],
            domain_ids=[3, 4],
        )

        await create_building(
            session=session,
            id=2,
            address="пр. Столыпина 27, Саратов",
            lat=51.531541,
            lon=46.027244,
        )
        await create_domain(
            session=session,
            id=5,
            parent_id=None,
            name="Техника",
        )
        await create_domain(
            session=session,
            id=6,
            parent_id=5,
            name="Ноутбуки",
        )
        await create_domain(
            session=session,
            id=7,
            parent_id=6,
            name="Сенсорные ноутбуки",
        )
        await create_organization(
            session=session,
            id=2,
            building_id=2,
            name="СИНЕЕ ЧЕРНОЕ",
            phone_numbers=["+79178894242"],
            domain_ids=[5],
        ) 
        await create_building(
            session=session,
            id=3,
            address="1206 Van Ness Ave, Fresno, CA 93721, USA",
            lat=36.737289,
            lon=-119.792144,
        )
        await create_organization(
            session=session,
            id=3,
            building_id=3,
            name="Lenovo",
            phone_numbers=["+19999999999"],
            domain_ids=[6],
        )


def run_web_api(
    address: Annotated[
        str,
        Parameter("--address", show_default=True),
    ] = "0.0.0.0:8000",
    workers: Annotated[
        str,
        Parameter("--workers", show_default=True),
    ] = "1",
) -> None:
    sys.argv = [
        "gunicorn",
        "--bind",
        address,
        "--workers",
        workers,
        "--worker-class",
        "uvicorn.workers.UvicornWorker",
        "test_task.web_api.app:create_web_api_app()",
    ]
    run_gunicorn()
