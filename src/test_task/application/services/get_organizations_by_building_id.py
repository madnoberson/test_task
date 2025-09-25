__all__ = ("get_organizations_by_building_id",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from test_task.application import view_models
from test_task.application.database_models import Organization, Domain
from test_task.application.converters import db_organization_to_view_model


async def get_organizations_by_building_id(
    session: AsyncSession,
    id_: int,
) -> list[view_models.Organization]:
    options = (
        selectinload(Organization.domains)
        .selectinload(Domain.children)
        .selectinload(Domain.children)
        .selectinload(Domain.children),
    )
    statement = (
        select(Organization)
        .where(Organization.building_id == id_)
        .options(*options)
        .limit(1)
    )

    view_models = []
    organizations = await session.scalars(statement)
    for organization in organizations:
        view_model = db_organization_to_view_model(
            organization=organization,
            exclude_building=True,
        )
        view_models.append(view_model)
    
    return view_models
