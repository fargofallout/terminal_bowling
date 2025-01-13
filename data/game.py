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

    def __repr__(self):
        return f"{self.id}: bowler: {self.bowler_id}, score: {self.score}, handicap: {self.handicap}, game number: {self.game_number}"

