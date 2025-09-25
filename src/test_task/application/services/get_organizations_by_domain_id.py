__all__ = ("get_organizations_by_domain_id",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select

from test_task.application import view_models
from test_task.application.database_models import Organization, Domain
from test_task.application.converters import db_organization_to_view_model


async def get_organizations_by_domain_id(
    session: AsyncSession,
    id_: int,
) -> list[view_models.Organization]:
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
        .where(Organization.domains.any(id=id_))
        .options(*options)
        .limit(1)
    )

    view_models = []
    organizations = await session.scalars(statement)
    for organization in organizations:
        view_model = db_organization_to_view_model(organization)
        view_models.append(view_model)
    
    return view_models
