from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Bowler(Base):
    __tablename__ = "bowler"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(30))
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    handicap: orm.Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.first_name} {self.last_name}, handicap: {self.handicap}"


class Team(Base):
    __tablename__ = "team"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    team_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))

    def __repr__(self) -> str:
        return f"id: {self.id}, team name: {self.team_name}"


class Season(Base):
    __tablename__ = "season"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)


