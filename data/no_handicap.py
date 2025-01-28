import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


class No_Handicap(SqlAlchemyBase):
    __tablename__ = "no_handicap_table"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    head_to_head_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("head_to_head_table.id"))
    head_to_head: orm.Mapped["Head_To_Head"] = orm.relationship(back_populates="User_Action_Numbers", lazy="joined")

    bowler_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("bowler_table.id"))
    bowler: orm.Mapped["Bowler"] = orm.relationship(back_populates="No_Handicap", lazy="joined")

