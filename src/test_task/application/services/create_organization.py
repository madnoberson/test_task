__all__ = ("create_organization",)

from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from test_task.application.database_models import (
    Organization,
    OrganizationPhone,
    organization_domains_table,
)


async def create_organization(
    session: AsyncSession,
    id: int,
    building_id: int | None, 
    name: str,
    phone_numbers: Iterable[str],
    domain_ids: Iterable[int],
) -> None:
    statement = insert(Organization).values(
        id=id,
        building_id=building_id,
        name=name,
    )
    await session.execute(statement)

    await _instert_organization_phones(
        session=session,
        organization_id=id,
        phone_numbers=phone_numbers,
    )
    await _insert_organization_domains(
        session=session,
        organization_id=id,
        domain_ids=domain_ids,
    )

    await session.commit()


async def _instert_organization_phones(
    session: AsyncSession,
    organization_id: int,
    phone_numbers: Iterable[str],
) -> None:
    organization_phones_as_dicts = [
        {"organization_id": organization_id, "number": phone_number}
        for phone_number in phone_numbers
    ]
    statement = (
        insert(OrganizationPhone)
        .values(organization_phones_as_dicts)
    )
    await session.execute(statement)


async def _insert_organization_domains(
    session: AsyncSession,
    organization_id: int,
    domain_ids: Iterable[int],
) -> None:
    organization_domains_as_dicts = [
        {"organization_id": organization_id, "domain_id": domain_id}
        for domain_id in domain_ids
    ]
    statement = (
        insert(organization_domains_table)
        .values(organization_domains_as_dicts)
    )
    await session.execute(statement)
