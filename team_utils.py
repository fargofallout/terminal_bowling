import regex
import sqlalchemy as sa

from data import db_session
from data.team import Team


def team_menu():

    return_to_main = False

    while not return_to_main:
        print(f"\n1 to add a new team")
        print(f"2 to list all teams")
        print(f"3 to modify a team")
        print(f"4 to delete a team")
        print(f"x to exit")

        user_choice = input(":").strip()

        match user_choice:
            case "1":
                print("\nenter team name")
                team_name = input(":").strip()
                new_team = create_team(team_name)
                print(f"new team: {new_team.id}: {new_team.team_name}")
            case "2":
                all_teams = get_all_teams()
                for each_team in all_teams:
                    print(each_team)
            case "x":
                return_to_main = True
            case _:
                print("not a valid choice, please try again")


def create_team(team_name):
    new_team = Team(team_name=team_name)
    session = db_session.create_session()

    try:
        session.add(new_team)
        session.commit()
        return new_team

    finally:
        session.close()


def get_all_teams():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Team).order_by(Team.id)).all()
        return result
    finally:
        session.close()


