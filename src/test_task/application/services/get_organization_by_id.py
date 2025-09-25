__all__ = ("get_organization_by_id",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select

from test_task.application import view_models
from test_task.application.database_models import Organization, Domain
from test_task.application.converters import db_organization_to_view_model


async def get_organization_by_id(
    session: AsyncSession,
    id_: int,
) -> view_models.Organization | None:
    load_domains_option = (
        selectinload(Organization.domains)
        .selectinload(Domain.children)
        .selectinload(Domain.children)
        .selectinload(Domain.children)
    ) 
    options = (
        joinedload(Organization.building),
        load_domains_option,
    )
    statement = (
        select(Organization)
        .where(Organization.id == id_)
        .options(*options)
        .limit(1)
    )

    organization = await session.scalar(statement)
    if not organization:
        return None
    
    view_model = db_organization_to_view_model(organization)
    return view_model
