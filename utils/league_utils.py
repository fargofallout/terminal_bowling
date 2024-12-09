import regex
import sqlalchemy as sa

from data import db_session
from data.league import League
from utils.alley_utils import get_alley_by_id
from utils.utils import parse_global_options


def league_menu():
    return_to_main = False
    while not return_to_main:
        # TODO: need to add the option to delete leagues
        print("\n****************************")
        print("NOTE: you will need to associate an alley with this league to be able to create it")
        print("****************************")
        print("1 to add a new league")
        print("2 to modify an existing league")
        print("'x' to return to main menu")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "1":
                create_league_menu()
            case "2":
                modify_league_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid input, please try again")


def create_league_menu():
    return_to_league_menu = False
    while not return_to_league_menu:
        print("\nenter alley id and league name in this format:")
        print("1 flaherty's tuesday nights")
        print("or 'x' to return to the main league menu")

        league_input = input(":").strip()
        if parse_global_options(league_input):
            continue

        match REqual(league_input):
            case "x" | "X":
                return_to_league_menu = True
            case r"^(\d+) +([^\n]+)$":
                league_match = regex.search(r"^(\d+) +([^\n]+)$", league_input)
                alley_id = league_match.group(1)
                league_name = league_match.group(2)
                print(f"alley: {alley_id}, league: {league_name}")
                alley = get_alley_by_id(alley_id)
                if not alley:
                    print("alley id does not exist, please try again")
                    continue
                new_league = create_league(league_name, alley_id)
                print(f"new league: {new_league}, alley: {new_league.alley}")
                return_to_league_menu = True
            case _:
                print("not a valid input, please try again")


def modify_league_menu():
    return_to_league_menu = False
    while not return_to_league_menu:
        # TODO: I don't like how this looks in the terminal
        print("\n*************************************************")
        print("to modify a league, use the format 'ml [league id] [new leauge name]', e.g.,")
        print("ml 5 new league name")
        print("*************************************************")
        print("to modify the alley associated with a league, use the format 'ma [league id] [new alley id]', e.g.,")
        print("ma 5 10")
        print("*************************************************")

        league_input = input(":").strip()
        if parse_global_options(league_input):
            continue

        match REqual(league_input):
            case "x" | "X":
                return_to_league_menu = True

            case r"^ml +(\d+) +([^\n]+)$":
                modify_league_match = regex.search(r"^ml +(\d+) +([^\n]+)$", league_input)
                league_id = modify_league_match.group(1)
                new_league_name = modify_league_match.group(2)
                league = get_league_by_id(league_id)
                if not league:
                    print("that league does not exist, please try again")
                    continue
                new_league = modify_league(league_id, new_name=new_league_name)
                if not new_league:
                    print("dammit, something went wrong changing the league name")
                return_to_league_menu = True

            case r"^ma +(\d+) +(\d+)$":
                modify_alley_match = regex.search(r"^ma +(\d+) +(\d+)$", league_input)
                league_id = modify_alley_match.group(1)
                new_alley_id = modify_alley_match.group(2)
                league = get_league_by_id(league_id)
                alley = get_alley_by_id(new_alley_id)
                if not league:
                    print("that league id is not valid, please try again")
                    continue
                if not alley:
                    print("that alley id is not valid, please try again")
                    continue
                new_league = modify_league(league_id, new_alley_id=new_alley_id)
                if not new_league:
                    print("dammit, not sure what could have went wrong with changing the league's alley")
                    continue
                actual_new_league = get_league_by_id(league_id)
                print(f"updated league info: {actual_new_league}")
                return_to_league_menu = True

            case _:
                print("not a valid input, please try again")


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
        league = session.scalars(sa.select(League).where(League.id==league_id)).one_or_none()
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
        league = session.scalars(sa.select(League).where(League.id==league_id)).unique().one_or_none()
        return league
    except Exception as e:
        print(f"can I catch whatever here? {e}")
    finally:
        session.close()


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)



