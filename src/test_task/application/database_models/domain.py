__all__ = ("Domain",)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint

from .base import Base


_parent_id_fk_constraint = ForeignKeyConstraint(
    ["parent_id"],
    ["domains.id"],
    ondelete="CASCADE",
)
_unique_constraint = UniqueConstraint("parent_id", "name")

_table_args = (_parent_id_fk_constraint, _unique_constraint)


class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = _table_args

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(nullable=True)
    name: Mapped[str]

    parent: Mapped["Domain"] = relationship(
        remote_side=lambda: [Domain.id],
        back_populates="children",
        lazy="noload",
    )
    children: Mapped[list["Domain"]] = relationship(
        back_populates="parent",
        lazy="noload",
    )
