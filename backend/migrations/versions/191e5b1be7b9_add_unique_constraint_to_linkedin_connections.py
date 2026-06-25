"""add unique constraint to linkedin connections

Revision ID: 191e5b1be7b9
Revises: 4e741f4caaef
Create Date: 2026-06-26 00:53:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '191e5b1be7b9'
down_revision: Union[str, Sequence[str], None] = '4e741f4caaef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the unique constraint that exists in the SQLAlchemy model
    # but was missing from the original linkedin_connections table migration
    op.create_unique_constraint(
        '_connection_uc',
        'linkedin_connections',
        ['first_name', 'last_name', 'company', 'position']
    )


def downgrade() -> None:
    op.drop_constraint(
        '_connection_uc',
        'linkedin_connections',
        type_='unique'
    )