__all__ = ("get_organizations_by_domain",)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select

from test_task.application import view_models
from test_task.application.database_models import Organization, Domain
from test_task.application.converters import db_organization_to_view_model


async def get_organizations_by_domain(
    session: AsyncSession,
    domain_name: str,
) -> list[view_models.Organization]:
    select_root_domains_statement = (
        select(Domain.id)
        .where(Domain.name.ilike(f"%{domain_name}%"))
        .cte("domain_tree", recursive=True)
    )
    select_child_domains_statement = (
        select(Domain.id)
        .where(Domain.parent_id == select_root_domains_statement.c.id)
    )
    domains = (
        select_root_domains_statement
        .union_all(select_child_domains_statement)
    )
    
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
        .join(Organization.domains)
        .where(Domain.id.in_(select(domains.c.id)))
        .options(*options)
        .distinct()
    )

    view_models = []
    organizations = await session.scalars(statement)
    for organization in organizations:
        view_model = db_organization_to_view_model(organization)
        view_models.append(view_model)
    
    return view_models 
