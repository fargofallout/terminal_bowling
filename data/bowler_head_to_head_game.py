import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class Bowler_Head_To_Head_Game(SqlAlchemyBase):
    __tablename__ = "bowler_head_to_head_game_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    bowler_position: orm.Mapped[int]
    game_number: orm.Mapped[int]

    left_bowler_scratch_score: orm.Mapped[int]
    left_bowler_handicap_score: orm.Mapped[int]
    right_bowler_scratch_score: orm.Mapped[int]
    right_bowler_handicap_score: orm.Mapped[int]

    left_bowler_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("bowler_table.id"))
    # left_bowler: orm.Mapped["Bowler"] = orm.relationship(back_populates="bowler_head_to_head_game", lazy="joined")

    right_bowler_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("bowler_table.id"))
    # right_bowler: orm.Mapped["Bowler"] = orm.relationship(back_populates="bowler_head_to_head_game", lazy="joined")

    head_to_head_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_table.id"))
    # TODO: figure out if this relationship is good
    # head_to_head: orm.Mapped["Head_To_Head"] = orm.relationship(back_populates="bowler_head_to_head_games", lazy="joined")

    head_to_head_game_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_game_table.id"))
    head_to_head_game: orm.Mapped["Head_To_Head_Game"] = orm.relationship(back_populates="bowler_head_to_head_games", lazy="joined")

