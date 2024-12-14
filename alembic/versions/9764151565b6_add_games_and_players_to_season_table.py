"""add games and players to season table

Revision ID: 9764151565b6
Revises: 
Create Date: 2024-12-13 13:01:15.756643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9764151565b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("season_table", sa.Column("games_per_week", sa.Integer))
    op.add_column("season_table", sa.Column("players_per_team", sa.Integer))


def downgrade() -> None:
    pass
