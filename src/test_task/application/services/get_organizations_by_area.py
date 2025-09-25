__all__ = (
    "Point",
    "Circle",
    "Rect",
    "Area",
    "get_organizations_by_area",
)

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, func

from test_task.application import view_models
from test_task.application.database_models import Organization, Building, Domain
from test_task.application.converters import db_organization_to_view_model


@dataclass
class Point:
    lat: float
    lon: float


@dataclass
class Circle:
    center: Point
    radius: float


@dataclass
class Rect:
    north_east: Point
    south_west: Point


type Area = Circle | Rect


async def get_organizations_by_area(
    session: AsyncSession,
    area: Area,
) -> list[view_models.Organization]:
    if isinstance(area, Circle):
        point = f"POINT({area.center.lon} {area.center.lat})"
        radius_in_meters = area.radius * 1000

        where_statement = func.ST_DWithin(
            Building.coordinates,
            func.ST_GeogFromText(point),
            radius_in_meters,
        )
    else:
        polygon = (
            f"POLYGON(({area.south_west.lon} {area.south_west.lat}, "
            f"{area.north_east.lon} {area.south_west.lat}, "
            f"{area.north_east.lon} {area.north_east.lat}, "
            f"{area.south_west.lon} {area.north_east.lat}, "
            f"{area.south_west.lon} {area.south_west.lat}))"
        )
        
        where_statement = func.ST_DWithin(
            Building.coordinates,
            func.ST_GeogFromText(polygon),
            0.0001,
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
        .join(Organization.building)
        .where(where_statement)
        .options(*options)
    )

    view_models = []
    organizations = await session.scalars(statement)
    for organization in organizations:
        view_model = db_organization_to_view_model(organization)
        view_models.append(view_model)
    
    return view_models
