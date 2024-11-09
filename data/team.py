import sqlalchemy as sa
from data.model_base import SqlAlchemyBase


class Team(SqlAlchemyBase):
    __tablename__ = "teams"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_name: str = sa.Column(sa.String, index=True)
