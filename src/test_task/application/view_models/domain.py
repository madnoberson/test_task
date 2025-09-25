__all__ = ("Domain",)

from typing import TypedDict


class Domain(TypedDict):
    id: int
    name: str
    children: list["Domain"]
