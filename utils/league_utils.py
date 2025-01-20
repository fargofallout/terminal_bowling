import sqlalchemy as sa

from data import db_session
from data.league import League


def create_league(league_name, alley_id):
    new_league = League(league_name=league_name, alley_id=alley_id)
    session = db_session.create_session()

    try:
        session.add(new_league)
        session.commit()
        alley_name = new_league.alley.alley_name
        return new_league
    finally:
        session.close()


def modify_league(league_id, new_name=None, new_alley_id=None):
    session = db_session.create_session()
    try:
        league = session.scalars(sa.select(League).where(League.id == league_id)).unique().one_or_none()
        if not league:
            print("not sure why I'd ever hit this since I check it in the menu function")
            return ""
        else:
            if new_name:
                league.league_name = new_name
            elif new_alley_id:
                league.alley_id = new_alley_id
            else:
                print("why would I ever hit this?")
        session.commit()
        return league
    finally:
        session.close()


def get_league_by_id(league_id):
    session = db_session.create_session()
    try:
        league = session.scalars(sa.select(League).where(League.id == league_id)).unique().one_or_none()
        return league
    except Exception as e:
        print(f"can I catch whatever here? {e}")
    finally:
        session.close()


def get_all_leagues():
    session = db_session.create_session()
    try:
        all_leagues = session.scalars(sa.select(League).order_by(League.id)).unique().all()
        return all_leagues
    finally:
        session.close()


def delete_league(league_id):
    session = db_session.create_session()
    try:
        league = session.scalars(sa.select(League).where(League.id == league_id)).unique().one_or_none()
        if league:
            session.delete(league)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()

