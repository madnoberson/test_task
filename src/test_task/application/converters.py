__all__ = ("db_organization_to_view_model",)

from geoalchemy2.shape import to_shape

from . import database_models
from . import view_models


def db_organization_to_view_model(
    organization: database_models.Organization,
    exclude_building: bool = False,
) -> view_models.Organization:
    domains = []
    for db_domain in organization.domains:
        domain = _db_domain_to_view_model(db_domain)
        domains.append(domain)

    mapping = {
        "id": organization.id,
        "name": organization.name,
        "phone_numbers": organization.phone_numbers,
        "domains": domains,
    }
    if not exclude_building:
        if organization.building:
            building = _db_building_to_view_model(organization.building)
        else:
            building = None
 
        mapping["building"] = building

    return view_models.Organization(**mapping)


def _db_domain_to_view_model(
    domain: database_models.Domain,
) -> view_models.Domain:
    children = []
    for child_db_domain in domain.children:
        child_domain = _db_domain_to_view_model(child_db_domain)
        children.append(child_domain)

    return view_models.Domain(
        id=domain.id,
        name=domain.name,
        children=children,
    )


def _db_building_to_view_model(
    building: database_models.Building,
) -> view_models.Building:
    x, y = to_shape(building.coordinates).xy
    lon, lat = x[0], y[0]

    return view_models.Building(
        id=building.id,
        address=building.address,
        lat=lat,
        lon=lon,
    )