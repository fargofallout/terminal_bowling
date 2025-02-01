import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional

from data.model_base import SqlAlchemyBase


class Season(SqlAlchemyBase):
    __tablename__ = "season_table"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    season_years: str = sa.Column(sa.String, index=True)
    handicap_formula: Mapped[str] = mapped_column(sa.String)
    games_per_week: Mapped[int]
    players_per_team: Mapped[int]
    is_complete: orm.Mapped[Optional[bool]]

    league_id: str = sa.Column(sa.String, sa.ForeignKey("league_table.id"))
    league: Mapped["League"] = relationship(back_populates="season", lazy="joined")

    head_to_heads: Mapped["Head_To_Head"] = relationship(back_populates="season", lazy="joined")

    def __repr__(self):
        return f"{self.id}, season: {self.season_years}, "\
            f"handicap formula: {self.handicap_formula}, "\
            f"games per week: {self.games_per_week}, "\
            f"players per team: {self.players_per_team}, "\
            f"complete? {self.is_complete}, " \
            f"league name: {self.league.league_name}"

