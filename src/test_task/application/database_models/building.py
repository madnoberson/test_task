__all__ = ("Building",)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from geoalchemy2 import Geography, WKBElement

from .base import Base


_geography = Geography(geometry_type="POINT", srid=4326)

_unique_constraint = UniqueConstraint("address", "coordinates")
_table_args = (_unique_constraint,)


class Building(Base):
    __tablename__ = "buildings"
    __table_args__ = _table_args

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    coordinates: Mapped[WKBElement] = mapped_column(_geography)
