import sqlalchemy as sa
from sqlalchemy.orm import relationship

from data.model_base import SqlAlchemyBase


class Season(SqlAlchemyBase):
    __tablename__ = "seasons"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    season_years: str = sa.Column(sa.String, index=True)

    league_id: str = sa.Column(sa.String, sa.ForeignKey("leagues.id"))
    # league: Mapped["League"] = relationship(back_populates="alley")

