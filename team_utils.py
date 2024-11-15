import regex
import sqlalchemy as sa

from data import db_session
from data.team import Team


def team_menu():

    return_to_main = False

    while not return_to_main:
        print(f"\n1 to add a new team") #done
        print(f"2 to list all teams") #done
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
            case "3":
                modify_team_menu()
            case "x":
                return_to_main = True
            case _:
                print("not a valid choice, please try again")


def modify_team_menu():
    class REqual(str):
        def __eq__(self, pattern):
            return regex.fullmatch(pattern, self)

    return_to_team_menu = False

    while not return_to_team_menu:
        print("\nenter the id of the team to modify")
        print("enter 'L' to list all teams")
        print("enter 'X' to exit")

        modify_input = input(":").strip()

        match REqual(modify_input):
            case "l" | "L":
                all_teams = get_all_teams()
                for each_team in all_teams:
                    print(f"{each_team}")
            case "x" | "X":
                return_to_team_menu = True
            case r"\d+":
                # CONTINUE HERE: check to make sure the team returned exists
                team_to_modify = get_team_by_id(int(modify_input))
                get_new_team_name_menu(modify_input)
            case _:
                print("not a valid option, please try again")


def get_new_team_name_menu(team_id):
    session = db_session.create_session()

    pass


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
        team = session.scalars(sa.select(Team).where(Team.id==team_id)).one_or_none()
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
        team = session.scalars(sa.select(Team).where(Team.id==team_id)).one_or_none()
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



