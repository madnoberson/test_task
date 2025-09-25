__all__ = ("create_building",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from test_task.application.database_models import Building


async def create_building(
    session: AsyncSession,
    id: int,
    address: str,
    lat: float,
    lon: float
) -> None:
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}.")
    
    point = f"POINT({lon} {lat})"

    statement = (
        insert(Building)
        .values(id=id, address=address, coordinates=point)
    )
    await session.execute(statement)

    await session.commit()
