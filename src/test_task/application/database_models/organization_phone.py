__all__ = ("OrganizationPhone",)

from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint

from .base import Base


_organization_id_fk_constraint = ForeignKeyConstraint(
    ["organization_id"],
    ["organizations.id"],
    ondelete="CASCADE",
)
_primary_key_constraint = PrimaryKeyConstraint(
    "organization_id",
    "number",
)

_table_args = (
    _organization_id_fk_constraint,
    _primary_key_constraint,
)


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    __table_args__ = _table_args

    organization_id: Mapped[int]
    number: Mapped[str]
