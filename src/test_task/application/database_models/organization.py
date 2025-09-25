__all__ = ("Organization", "organization_domains_table")

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from .base import Base
from .building import Building
from .domain import Domain
from .organization_phone import OrganizationPhone


organization_domains_table = Table(
    "organization_domains",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id", ondelete="CASCADE")),
    Column("domain_id", ForeignKey("domains.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("organization_id", "domain_id"),
)

_building_id_fk_constraint = ForeignKeyConstraint(
    ["building_id"],
    ["buildings.id"],
    ondelete="SET NULL",
)
_table_args = (_building_id_fk_constraint,)


class Organization(Base):
    __tablename__ = "organizations"
    __table_args__ = _table_args

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int | None] = mapped_column(nullable=True)
    name: Mapped[str]

    phones: Mapped[list[OrganizationPhone]] = relationship(
        lazy="selectin",
    ) 
    building: Mapped[Building | None] = relationship(
        lazy="noload",
    )
    domains: Mapped[list[Domain]] = relationship(
        secondary=organization_domains_table,
        lazy="noload",
    )

    @property
    def phone_numbers(self) -> list[str]:
        return [phone.number for phone in self.phones]
