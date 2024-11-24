import regex
import sqlalchemy as sa

from data import db_session
from data.league import League
from utils.alley_utils import get_alley_by_id, get_all_alleys


def league_menu():
    return_to_main = False
    while not return_to_main:
        print("\n****************************")
        print("NOTE: you will need to associate an alley with this league to be able to create it")
        print("****************************")
        print("1 to add a new league")
        print("2 to modify an existing league")
        print("'l' to list existing leagues")
        print("'a' to list existing alleys")
        print("'x' to return to main menu")

        user_choice = input(":").strip()

        match user_choice:
            case "1":
                create_league_menu()
            case "2":
                modify_league_menu()
            case "l" | "L":
                all_leagues = get_all_leagues()
                print("****************************")
                for each_league in all_leagues:
                    print(f"{each_league}")
                print("****************************")
            case "a" | "A":
                all_alleys = get_all_alleys()
                print("****************************")
                for each_alley in all_alleys:
                    print(f"{each_alley}")
                print("****************************")
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid input, please try again")


def create_league_menu():
    return_to_league_menu = False
    print("\nenter alley id and league name in this format:")
    print("1 flaherty's tuesday nights")
    print("or 'x' to return to the main league menu")
    league_input = input(":").strip()
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
            else:
                new_league = create_league(league_name, alley_id)
                print(f"new league: {new_league}, alley: {new_league.alley}")
                return_to_league_menu = True
        case _:
            print("not a valid input, please try again")


def modify_league_menu():
    return_to_league_menu = False
    # CONTINUE HERE: I think I'm going to create a function that takes in certain letters and 
    # spits out a list of that item, so then it can be a global thing and I don't have to 
    # list the options for listing leagues or whatever over and over again
    # not sure how I'd make it truly global, though - it seems like I'd still have to account
    # for it on every match statement - hmmmmmmmmm
    print("\n'l' to list leagues")
    print("'m' to list alleys")
    print("*********")
    print("to modify a league, use the format 'ml [league id] [new leauge name]', e.g.,")
    print("ml 5 new league name")
    print("*********")
    print("to modify the alley associated with a league, use the format 'ma [league id] [new alley id]', e.g.,")
    print("ma 5 10")
    print("*********")
    league_input = input(":").strip()

    match REqual(league_input):
        case "l" | "L":
            print("listing leagues")
        case "a" | "A":
            print("listing alleys")
        case "x" | "X":
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


def get_all_leagues():
    session = db_session.create_session()

    try:
        all_leagues = session.scalars(sa.select(League).order_by(League.id)).all()
        return all_leagues
    finally:
        session.close()


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self)



