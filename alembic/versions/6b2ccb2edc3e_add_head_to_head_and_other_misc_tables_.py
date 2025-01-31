"""add head_to_head and other misc tables, add various fields

Revision ID: 6b2ccb2edc3e
Revises: 1dca93bb8f54
Create Date: 2025-01-31 03:18:12.164505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b2ccb2edc3e'
down_revision: Union[str, None] = '1dca93bb8f54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("game_table", sa.Column("head_to_head_id", sa.String))
    op.add_column("game_table", sa.Column("team_id", sa.Integer))
    op.drop_column("game_table", "game_number")

    op.create_table("no_handicap_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("head_to_head_id", sa.Integer, sa.ForeignKey("head_to_head_table.id")),
        sa.Column("bowler_id", sa.Integer, sa.ForeignKey("bowler_table.id")))

    op.create_table("head_to_head_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("left_team_id", sa.Integer, sa.ForeignKey("team_table.id")),
        sa.Column("right_team_id", sa.Integer, sa.ForeignKey("team_table.id")),
        sa.Column("season_id", sa.Integer, sa.ForeignKey("season_table.id")))

    op.create_table("head_to_head_game_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("left_team_scratch_score", sa.Integer),
        sa.Column("left_team_handicap_score", sa.Integer),
        sa.Column("right_team_scratch_score", sa.Integer),
        sa.Column("right_team_handicap_score", sa.Integer),
        sa.Column("left_team_id", sa.Integer, sa.ForeignKey("team_table.id")),
        sa.Column("right_team_id", sa.Integer, sa.ForeignKey("team_table.id")),
        sa.Column("head_to_head_id", sa.Integer, sa.ForeignKey("head_to_head_table.id")))

    op.create_table("user_action_numbers_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("action_number", sa.Integer),
        sa.Column("item_id", sa.Integer),
        sa.Column("item_string", sa.String),
        sa.Column("head_to_head_id", sa.Integer, sa.ForeignKey("head_to_head_table.id")))

    op.create_table("bowler_head_to_head_game_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("bowler_position", sa.Integer),
        sa.Column("game_number", sa.Integer),
        sa.Column("left_bolwer_scratch_score", sa.Integer),
        sa.Column("left_bolwer_handicap_score", sa.Integer),
        sa.Column("right_bolwer_scratch_score", sa.Integer),
        sa.Column("right_bolwer_handicap_score", sa.Integer),
        sa.Column("left_bowler_id", sa.Integer, sa.ForeignKey("bowler_table.id")),
        sa.Column("right_bowler_id", sa.Integer, sa.ForeignKey("bowler_table.id")),
        sa.Column("head_to_head_id", sa.Integer, sa.ForeignKey("head_to_head_table.id")))


def downgrade() -> None:
    pass
