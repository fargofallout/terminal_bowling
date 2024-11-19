import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class League(SqlAlchemyBase):
    __tablename__ = "leagues"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    league_name: str = sa.Column(sa.String, index=True)

    alley_id: str = sa.Column(sa.String, sa.ForeignKey("alley.id"), index=True)
    alley = orm.Relationship("Alley", back_populates="leagues")

    def __repr__(self):
        return f"{self.id}: {self.league_name}"

