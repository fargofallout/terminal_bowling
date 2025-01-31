import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import Optional

from data.model_base import SqlAlchemyBase


class Team(SqlAlchemyBase):
    __tablename__ = "team_table"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_name: str = sa.Column(sa.String, index=True)

    games: orm.Mapped[Optional["Game"]] = orm.relationship(back_populates="team")

    def __repr__(self):
        return f"{self.id}: {self.team_name}"

