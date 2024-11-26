import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from data.model_base import SqlAlchemyBase


class Season(SqlAlchemyBase):
    __tablename__ = "season_table"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    season_years: str = sa.Column(sa.String, index=True)

    league_id: str = sa.Column(sa.String, sa.ForeignKey("league_table.id"))
    league: Mapped["League"] = relationship(back_populates="season", lazy="joined")


