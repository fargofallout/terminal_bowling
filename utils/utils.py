import sqlalchemy as sa

from data import db_session
from data.bowler import Bowler
from data.team import Team
from data.alley import Alley


def parse_global_options(user_input):
    match user_input:
        case "b" | "B":
            all_bowlers = get_all_bowlers()
            print("****************************")
            for each_bowler in all_bowlers:
                print(each_bowler)
            print("****************************")
            return True
        case "t" | "T":
            all_teams = get_all_teams()
            print("****************************")
            for each_team in all_teams:
                print(each_team)
            print("****************************")
            return True
        case "a" | "A":
            all_alleys = get_all_alleys()
            print("****************************")
            for each_alley in all_alleys:
                print(each_alley)
            print("****************************")
            return True
        case _:
            return False


def get_all_bowlers():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Bowler).order_by(Bowler.id)).all()
        return result
    finally:
        session.close()


def get_all_teams():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Team).order_by(Team.id)).all()
        return result
    finally:
        session.close()


def get_all_alleys():
    session = db_session.create_session()
    try:
        all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).all()
        return all_alleys
    finally:
        session.close()



