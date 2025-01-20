import regex
import sqlalchemy as sa

from data import db_session
from data.team import Team


def create_team(team_name):
    new_team = Team(team_name=team_name)
    session = db_session.create_session()

    try:
        session.add(new_team)
        session.commit()
        return new_team

    finally:
        session.close()


def modify_team(team_id, new_team_name):
    session = db_session.create_session()

    try:
        team = session.scalars(sa.select(Team).where(Team.id == team_id)).one_or_none()
        if not team:
            return ""
        else:
            team.team_name = new_team_name
            session.commit()
            return team
    finally:
        session.close()


def get_team_by_id(team_id):
    session = db_session.create_session()
    try:
        team = session.scalars(sa.select(Team).where(Team.id == team_id)).one_or_none()
        return team
    finally:
        session.close()


def get_all_teams():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Team).order_by(Team.id)).all()
        return result
    finally:
        session.close()


def delete_team(team_id):
    session = db_session.create_session()

    try:
        team = session.scalars(sa.select(Team).where(Team.id == team_id)).one_or_none()
        if team:
            session.delete(team)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


