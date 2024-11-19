import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from data.model_base import SqlAlchemyBase
from data.league import League


class Alley(SqlAlchemyBase):
    __tablename__ = "alley"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    alley_name: Mapped[str] = mapped_column(index=True)
    # alley_name: str = sa.Column(sa.String, index=True)
    alley_city: Mapped[str] = mapped_column(index=True)
    # alley_city: str = sa.Column(sa.String, index=True)

    leagues: Mapped[list["League"]] = relationship(back_populates="alley")

    def __repr__(self):
        if self.alley_city:
            return f"{self.id}: {self.alley_name}, {self.alley_city}"
        else:
            return f"{self.id}: {self.alley_name}"

