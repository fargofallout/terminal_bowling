import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class Head_To_Head(SqlAlchemyBase):
    __tablename__ = "head_to_head_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    week_number: orm.Mapped[int]
    week_complete: orm.Mapped[bool]

    left_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))
    # TODO: figure out if these relationships need to exist
    # left_team: orm.Mapped["Team"] = orm.relationship(back_populates="head_to_head", lazy="joined")
    right_team_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("team_table.id"))
    # right_team: orm.Mapped["Team"] = orm.relationship(back_populates="head_to_head", lazy="joined")

    season_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("season_table.id"))
    season: orm.Mapped["Season"] = orm.relationship(back_populates="head_to_head", lazy="joined")

    user_action_numbers: orm.Mapped[list["User_Action_Numbers"]] = orm.relationship(back_populates="head_to_head", lazy="joined")

    no_handicap: orm.Mapped[list["No_Handicap"]] = orm.relationship(back_populates="head_to_head", lazy="joined")

    head_to_head_games: orm.Mapped[list["Head_To_Head_Game"]] = orm.relationship(back_populates="head_to_head", lazy="joined")

    games: orm.Mapped[list["Game"]] = orm.relationship(back_populates="head_to_head", lazy="joined")

    def __repr__(self):
        return f"wtf"

