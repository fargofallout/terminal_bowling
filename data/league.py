import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from data.model_base import SqlAlchemyBase


class League(SqlAlchemyBase):
    __tablename__ = "league_table"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    league_name: str = sa.Column(sa.String, index=True)

    alley_id: str = sa.Column(sa.String, sa.ForeignKey("alley_table.id"), index=True)
    # alley = orm.Relationship("Alley", back_populates="leagues")
    alley: Mapped["Alley"] = relationship(back_populates="leagues", lazy="joined")

    season: Mapped["Season"] = relationship(back_populates="league", lazy="joined")

    def __repr__(self):
        return f"{self.id}: {self.league_name}, alley: {self.alley}"

