__all__ = ("Organization",)

from typing import TypedDict, NotRequired

from .building import Building
from .domain import Domain


class Organization(TypedDict):
    id: int
    name: str
    phone_numbers: list[str]
    domains: list[Domain]
    building: NotRequired[Building | None]
