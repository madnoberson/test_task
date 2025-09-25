__all__ = ("router",)

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from test_task import application
from test_task.application import Point, Rect, Circle, Area
from test_task.application import view_models
from .stub import Stub
from .api_key_verifier import verify_api_key


router = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])

_Session = Annotated[AsyncSession, Depends(Stub(AsyncSession))]


@router.get("/organizations/by-name")
async def get_organization_by_name(
    session: _Session,
    name: Annotated[str, Query()],
) -> view_models.Organization | None:
    """
    Returns an organization by its exact name
    (case-insensative).
    """
    return await application.get_organization_by_name(
        session=session,
        name=name,
    )


@router.get("/organizations/{organization_id}")
async def get_organization_by_id(
    session: _Session,
    organization_id: int,
) -> view_models.Organization | None:
    """
    Returns an organization by its id.
    """
    return await application.get_organization_by_id(
        session=session,
        id_=organization_id,
    )


@router.get("/domains/{domain_id}/organizations")
async def get_organizations_by_domain_id(
    session: _Session,
    domain_id: int,
) -> list[view_models.Organization]:
    """
    Returns organizations belonging to a specific domain
    by domain id.
    """
    return await application.get_organizations_by_domain_id(
        session=session,
        id_=domain_id,
    )


@router.get("/buildings/{building_id}/organizations")
async def get_organizations_by_building_id(
    session: _Session,
    building_id: int,
) -> list[view_models.Organization]:
    """
    Returns organizations located in a specific building
    by building id. 
    """
    return await application.get_organizations_by_building_id(
        session=session,
        id_=building_id,
    )



@router.get("/organizations/search/by-area")
async def get_organizations_by_area(
    session: _Session,
    center_lat: Annotated[float | None, Query()] = None,
    center_lon: Annotated[float | None, Query()] = None,
    radius: Annotated[float | None, Query()] = None,
    north_east_lat: Annotated[float | None, Query()] = None,
    north_east_lon: Annotated[float | None, Query()] = None,
    south_west_lat: Annotated[float | None, Query()] = None,
    south_west_lon: Annotated[float | None, Query()] = None,
) -> list[view_models.Organization]:
    """
    Returns organizations whose buildings are located within
    the provided area.

    The area can be defined in one of two ways:

    1. **Circle:**. Using `center_lat`, `center_lon` and `radius`
       parameters.
    2. **Rectangle:** Using `north_east_lat`, `north_east_lon`,
       `south_west_lat` and `south_west_lon` parameters.
    
    Errors:
        400: If the provided parameters are insufficient
             to define a valid area.
    """
    area: Area

    if (
        center_lat is not None
        and center_lon is not None
        and radius is not None
    ):
        center = Point(lat=center_lat, lon=center_lon)
        area = Circle(center=center, radius=radius)
    
    elif (
        north_east_lat is not None
        and north_east_lon is not None
        and south_west_lat is not None
        and south_west_lon is not None
    ):
        north_east = Point(lat=north_east_lat, lon=north_east_lon)
        south_west = Point(lat=south_west_lat, lon=south_west_lon)
        area = Rect(north_east=north_east, south_west=south_west)
    
    else:
        raise HTTPException(400, "Invliad query paramaters.")

    return await application.get_organizations_by_area(
        session=session,
        area=area,
    )


@router.get("/organizations/search/by-domain")
async def get_organizations_by_domain(
    session: _Session,
    domain: Annotated[str, Query()],
) -> list[view_models.Organization]:
    """
    Returns organizations by domain with hierarchical search.
    
    Searches for organizations by domain using hierarchical
    matching. For example, searching for the domain "Food"
    (top-level) will return all organizations belonging to
    "Food" and its subdomains like "Meat products",
    "Dairy products", etc.

    The search is case-insensative and supports partial
    matching - you can specify only part of the domain
    name.
    """
    return await application.get_organizations_by_domain(
        session=session,
        domain_name=domain,
    )
