__all__ = ("create_domain",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from test_task.application.database_models import Domain


async def create_domain(
    session: AsyncSession,
    id: int,
    parent_id: int | None,
    name: str,
) -> None:
    statemenet = insert(Domain).values(
        id=id,
        parent_id=parent_id,
        name=name,
    )
    await session.execute(statemenet)