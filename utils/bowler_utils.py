import regex
import sqlalchemy as sa

from data.bowler import Bowler
from data import db_session


def create_bowler(first_name, last_name):
    new_bowler = Bowler(first_name=first_name, last_name=last_name)
    session = db_session.create_session()

    try:
        session.add(new_bowler)
        session.commit()
        return f"{new_bowler.id} {new_bowler.first_name} {new_bowler.last_name}"
    finally:
        session.close()


def delete_bowler(id):
    session = db_session.create_session()

    try:
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id==id)).unique().one_or_none()
        if bowler:
            session.delete(bowler)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()


def get_bowler_by_id(id):
    session = db_session.create_session()
    try:
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id==id)).unique().one_or_none()
        # print(f"here's that bowler: {bowler}")
        # print(f"id? {bowler.id}")
        return bowler
    finally:
        session.close()


def get_all_bowlers():
    session = db_session.create_session()
    try:
        all_bowlers = session.scalars(sa.select(Bowler)).unique().all()
        return all_bowlers
    finally:
        session.close()


def modify_bowler(bowler_id, new_first_name, new_last_name):
    session = db_session.create_session()

    try:
        # session.execute(sa.update(Bowler),[{"id":bowler_id, "first_name": new_first_name, "last_name": new_last_name},],)
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id == bowler_id)).unique().one_or_none()
        if not bowler:
            return ""
        else:
            bowler.first_name = new_first_name
            bowler.last_name = new_last_name
            session.commit()
            return bowler

    finally:
        session.close()


#this idea is courtesy https://discuss.python.org/t/structural-pattern-matching-should-permit-regex-string-matches/22700/8
class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


