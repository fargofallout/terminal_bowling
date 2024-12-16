import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class Bowler(SqlAlchemyBase):
    __tablename__ = "bowler_table"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name: str = sa.Column(sa.String, index=True)
    last_name: str = sa.Column(sa.String, index=True)

    game: orm.Mapped[list["Game"]] = orm.relationship(back_populates="bowler", lazy="joined")


    def __repr__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"

