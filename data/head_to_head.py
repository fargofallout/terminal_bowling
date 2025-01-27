import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class Head_To_Head(SqlAlchemyBase):
    __tablename__ = "head_to_head_table"

    # CONTINUE HERE: need to create an alembic upgrade for this
    # but also need to figure out how to store information such as positions of data 
    # on the score sheet, and whether a bowler does not yet have a handicap - 
    # I'm thinking of doing a json column on this table, but need to mull it over
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    week_number: orm.Mapped[int]
    week_complete: orm.Mapped[bool]

    left_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))
    left_team: orm.Mapped["Team"] = orm.relationship(back_populates="team", lazy="joined")
    right_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))
    right_team: orm.Mapped["Team"] = orm.relationship(back_populates="team", lazy="joined")

    season_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("season_table.id"))
    season: orm.Mapped["Season"] = orm.relationship(back_populates="season", lazy="joined")

    def __repr__(self):
        return f"wtf"

