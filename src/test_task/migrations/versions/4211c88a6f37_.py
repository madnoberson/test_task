"""
Create 'buildings' table, create 'domains' table,
create 'organizations' table, create 'organization_phones'
table, create 'organization_domains' table.

Revision ID: 4211c88a6f37
Revises: 
Create Date: 2025-09-24 06:41:56.984388
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


# revision identifiers, used by Alembic.
revision: str = '4211c88a6f37'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("coordinates", Geography(geometry_type="POINT", srid=4326), nullable=False),
    )
    op.create_table(
        "domains",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["domains.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("building_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"], ondelete="SET NULL"),
    )
    op.create_table(
        "organization_domains",
        sa.Column("organization_id", sa.Integer()),
        sa.Column("domain_id", sa.Integer()),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("organization_id", "domain_id"),
    )
    op.create_table(
        "organization_phones",
        sa.Column("organization_id", sa.Integer()),
        sa.Column("number", sa.String()),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("organization_id", "number"),
    )


def downgrade() -> None:
    op.drop_table("organization_phones")
    op.drop_table("organization_domains")
    op.drop_table("organizations") 
    op.drop_table("domains")
    op.drop_table("buildings")
