import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import Optional

from data.model_base import SqlAlchemyBase


# hold data about each team's scores
# need to add a game number to this?
class Head_To_Head_Game(SqlAlchemyBase):
    __tablename__ = "head_to_head_game_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    game_number: orm.Mapped[int]

    left_team_scratch_score: orm.Mapped[int]
    left_team_handicap_score: orm.Mapped[int]
    right_team_scratch_score: orm.Mapped[int]
    right_team_handicap_score: orm.Mapped[int]

    left_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))
    right_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))

    head_to_head_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_table.id"))
    head_to_head: orm.Mapped["Head_To_Head"] = orm.relationship(back_populates="head_to_head_games")

    bowler_head_to_head_games: orm.Mapped[list["Bowler_Head_To_Head_Game"]] = orm.Relationship(back_populates="head_to_head_game", lazy="joined")

