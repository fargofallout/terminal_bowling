import regex
import sqlalchemy as sa

from data import db_session
from data.league import League


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
                print("\nenter alley id and league name in this format:")
                print("1 flaherty's tuesday nights")
                league_regex = regex.compile(r"^(\d+) +([^\n]+)$")
                league_input = input(":").strip()
                league_match = league_regex.search(league_input)
                if not league_match:
                    print("that input is invalid, please try again")
                else:
                    print(f"id: {league_match.group(1)}, league name: {league_match.group(2)}")
                    league_name = league_match.group(2)
                    alley_id = league_match.group(1)
                    new_league = create_league(league_name=league_name, alley_id=alley_id)
                print(f"")
            case "l" | "L":
                all_leagues = get_all_leagues()
                for each_league in all_leagues:
                    print(f"{each_league}")
            case "x" | "X":
                return_to_main = True


def create_league(league_name, alley_id):
    new_league = League(league_name=league_name, alley_id=alley_id)
    session = db_session.create_session()

    try:
        session.add(new_league)
        session.commit()
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


