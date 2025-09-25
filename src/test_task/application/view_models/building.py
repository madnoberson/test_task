__all__ = ("Building",)

from typing import TypedDict


class Building(TypedDict):
    id: int
    address: str
    lat: float
    lon: float