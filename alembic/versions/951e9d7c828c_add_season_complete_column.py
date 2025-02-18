"""add season complete column

Revision ID: 951e9d7c828c
Revises: 7a2cc0385bcc
Create Date: 2025-02-01 16:50:34.860007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '951e9d7c828c'
down_revision: Union[str, None] = '7a2cc0385bcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("season_table", sa.Column("is_complete", sa.Boolean, nullable=True))


def downgrade() -> None:
    op.drop_column("season_table", "is_complete")
