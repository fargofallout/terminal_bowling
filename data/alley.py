import sqlalchemy as sa

from data.model_base import SqlAlchemyBase


class Alley(SqlAlchemyBase):
    __tablename__ = "alley"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    alley_name: str = sa.Column(sa.String, index=True)
    alley_city: str = sa.Column(sa.String, index=True)

    def __repr__(self):
        if self.alley_city:
            return f"{self.id}: {self.alley_name}, {self.alley_city}"
        else:
            return f"{self.id}: {self.alley_name}"

