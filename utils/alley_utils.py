import sqlalchemy as sa

from data import db_session
from data.alley import Alley


def add_alley(alley_name, city_name=None):
    new_alley = Alley(alley_name=alley_name, alley_city=city_name)
    session = db_session.create_session()

    try:
        session.add(new_alley)
        session.commit()
        return new_alley
    finally:
        session.close()


def modify_alley(alley_id, new_name=None, new_city=None):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id == alley_id)).unique().one_or_none()
        if not alley:
            return ""
        else:
            if new_name and not new_city:
                alley.alley_name = new_name
            elif new_city and not new_name:
                alley.alley_city = new_city
            else:
                alley.alley_name = new_name
                alley.alley_city = new_city
            session.commit()
            return alley
    finally:
        session.close()


def get_alley_by_id(alley_id):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id == alley_id)).unique().one_or_none()
        return alley
    finally:
        session.close()


def get_all_alleys():
    session = db_session.create_session()
    try:
        all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).unique().all()
        return all_alleys
    finally:
        session.close()


def delete_alley(alley_id):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id == alley_id)).unique().one_or_none()
        if not alley:
            return False
        else:
            session.delete(alley)
            session.commit()
            return True
    finally:
        session.close()

