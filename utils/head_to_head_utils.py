import sqlalchemy as sa

from data import db_session
from data.head_to_head import Head_To_Head


def create_head_to_head(week_number, left_team_id, right_team_id, season_id):

    new_head_to_head = Head_To_Head(week_number=week_number,
                                    week_complete=False,
                                    left_team_id=left_team_id,
                                    right_team_id=right_team_id,
                                    season_id=season_id)

    session = db_session.create_session()

    try:
        session.add(new_head_to_head)
        session.commit()
        return new_head_to_head
    finally:
        session.close()


def get_head_to_head_by_id(head_to_head_id):
    session = db_session.create_session()
    try:
        head_to_head = session.scalars(sa.select(Head_To_Head).where(Head_To_Head.id == head_to_head_id)).unique().one_or_none()
        return head_to_head
    finally:
        session.close()

