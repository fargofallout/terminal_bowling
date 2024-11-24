import regex
import sqlalchemy as sa

from data import db_session
from data.team import Team
from utils.utils import parse_global_options


def team_menu():

    return_to_main = False

    while not return_to_main:
        print(f"\n1 to add a new team") #done
        print(f"2 to modify a team") #done
        print(f"3 to delete a team") #done
        print(f"x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "1":
                print("\nenter team name")
                team_name = input(":").strip()
                new_team = create_team(team_name)
                print(f"new team: {new_team.id}: {new_team.team_name}")
            case "2":
                modify_team_menu()
            case "3":
                delete_team_menu()
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
        print("enter 'X' to exit")

        modify_input = input(":").strip()
        if parse_global_options(modify_input):
            continue

        match REqual(modify_input):
            case "x" | "X":
                return_to_team_menu = True
            case r"\d+":
                team_to_modify = get_team_by_id(int(modify_input))
                if team_to_modify:
                    get_new_team_name_menu(team_to_modify)
                else:
                    print("that team doesn't exist, please try again")
            case _:
                print("not a valid option, please try again")


def get_new_team_name_menu(team_to_modify):
    return_to_modify_menu = False

    while not return_to_modify_menu:
        print("\n****************************")
        print(f"the team you're modifying is {team_to_modify}")
        print("****************************")
        print(f"enter the the new name")
        print(f"or enter 'x' to return to the previous menu")
        print(f"(if the team name is 'x', then I guess I'll have to think about how to handle that)")
        user_choice = input(":").strip()

        match user_choice:
            case "x" | "X":
                return_to_modify_menu = True
            case _:
                new_team_name = modify_team(team_to_modify.id, user_choice)
                if not new_team_name:
                    print("it inexplicably wasn't found, even though I checked it once")
                else:
                    print(f"new team name: {new_team_name.team_name}")
                    return_to_modify_menu = True


def delete_team_menu():
    class REqual(str):
        def __eq__(self, pattern):
            return regex.fullmatch(pattern, self)

    return_to_team_menu = False

    while not return_to_team_menu:
        print("\nenter the team's id to delete them")
        print("enter 'x' to return to the previous menu")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match REqual(user_choice):
            case r"\d+":
                successful_deletion = delete_team(user_choice)
                if successful_deletion:
                    print("team has been deleted")
                    return_to_team_menu = True
                else:
                    print(f"that id wasn't found - please try again")

            case "x" | "X":
                return_to_team_menu = True
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


def delete_team(team_id):
    session = db_session.create_session()

    try:
        team = session.scalars(sa.select(Team).where(Team.id==team_id)).one_or_none()
        if team:
            session.delete(team)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()

