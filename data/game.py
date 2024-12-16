import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = "game_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    score: orm.Mapped[int]
    handicap: orm.Mapped[int]
    game_number: orm.Mapped[int]

    bowler_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("bowler_table.id"))
    bowler: orm.Mapped["Bowler"] = orm.relationship(back_populates="game", lazy="joined")

