import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class User_Action_Numbers(SqlAlchemyBase):
    __tablename__ = "user_action_numbers_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    head_to_head_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_table.id"))
    head_to_head: orm.Mapped["Head_To_Head"] = orm.relationship(back_populates="User_Action_Numbers", lazy="joined")

    # CONTINUE HERE: need to figure out if this table is going to have ids for games, bowlers, teams, etc., and
    # when a user enters a number o modify something, it figures out which value is set for that row?

