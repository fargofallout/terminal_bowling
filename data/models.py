import sqlalchemy as sa
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Bowler(Base):
    __tablename__ = "bowler"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(30))

    def __repr__(self) -> str:
        return f"id: {self.id}, first name: {self.first_name}"

class Team(Base):
    __tablename__ = "team"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    team_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))

    def __repr__(self) -> str:
        return f"id: {self.id}, team name: {self.team_name}"

