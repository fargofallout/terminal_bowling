import sqlalchemy as sa

from data.model_base import SqlAlchemyBase


class Bowler(SqlAlchemyBase):
    __tablename__ = "bowlers"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name: str = sa.Column(sa.String, index=True)
    last_name: str = sa.Column(sa.String, index=True)

    def __repr__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"

