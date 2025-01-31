import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class User_Action_Numbers(SqlAlchemyBase):
    __tablename__ = "user_action_numbers_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    action_number: orm.Mapped[int]
    item_id: orm.Mapped[int]
    item_string: orm.Mapped[str]

    head_to_head_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_table.id"))
    head_to_head: orm.Mapped["Head_To_Head"] = orm.relationship(back_populates="user_action_numbers", lazy="joined")

