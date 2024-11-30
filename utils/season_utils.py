import regex
import sqlalchemy as sa
import json

from data import db_session
from data.season import Season
from utils.utils import parse_global_options, parse_formula, recursive_calc_function
from utils.league_utils import get_league_by_id


def season_menu():
    return_to_main = False
    while not return_to_main:
        print("\n1 to enter a new season")
        print("2 to modify an existing season")
        print("3 to delete an existing season")
        print("'x' to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "x" | "X":
                return_to_main = True
            case "1":
                new_season_menu()
            case "2":
                modify_season_menu()
            case _:
                print("not a valid input, please try again")


def new_season_menu():
    return_to_season_menu = False
    while not return_to_season_menu:
        print("\n***********************************************")
        print("note: a season has to be attached to a league")
        print("enter these three parts of a season: [league id] [season timeframe] [handicap formula]")
        print("in this format: 1 [2024-2025] ((220 - average) * 0.9)")
        print("more notes: put the season timeframe in square brackets and the formula in parentheses")
        print("for the formula, make sure to wrap each pair of values in parentheses")
        print("I'm omly accepting one unique variable, but if I ever encounter something else in a league, I'll deal with it")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        match REqual(user_input):
            case "x" | "X":
                return_to_season_menu = True
            # user input is in this format: 1 [timeframe] (formula)
            case r"^(\d+) +\[([^\n\[\]]+)\] +\(([^\n]+)\)$":
                season_match = regex.search("^(\d+) +\[([^\n\[\]]+)\] +\(([^\n]+)\)$", user_input)
                league_id = season_match.group(1)
                season_timeframe = season_match.group(2)
                handicap_formula = season_match.group(3)
                league = get_league_by_id(league_id)
                if not league:
                    print("not a valid league id, please try again")
                    continue

                # token_list will be something like ['(', '220', '-', 'avg', ')', '*', '0.90']
                token_list = parse_formula(handicap_formula)
                if not token_list:
                    print("something went wrong with parsing the formula (hopefully I printed the problem)")
                    print("please try again")
                    continue

                print("formula passed validation - please enter a sample average to see what the handicap returned is")

                provided_numerical_average = False
                while not provided_numerical_average:
                    sample_average = input(":").strip()
                    if not regex.search(r"^\d+$", sample_average):
                        print("that's not a valid number to test, please try again, or enter 'x' if you want to bail")

                    if sample_average in ["x", "X"]:
                        break

                    if regex.search(r"^\d+$", sample_average):
                        calculated_handicap = recursive_calc_function(token_list, int(sample_average))
                        print(f"moment of truth: {calculated_handicap}")
                        return_to_season_menu = True
                        provided_numerical_average = True
                        new_season = create_season(season_timeframe, token_list, league_id)
                        print(f"{new_season}")

            case _:
                print("that's not a valid input, please try again")


def modify_season_menu():
    return_to_season_menu = False
    while not return_to_season_menu:
        print("\nenter 1 to modify a season's timeframe")
        print("enter 2 to modify a season's handicap formula")
        print("enter 3 to change a season's league")
        print("enter 'x' to return to the main season menu")

        season_input = input(":").strip()
        if parse_global_options(season_input):
            continue

        match season_input:
            case "1":
                print("modifying a the years")
            case "2":
                print("modifying the formula")
            case "3":
                print("modifying the league")
            case "x" | "X":
                return_to_season_menu = True
            case _:
                print("not a valid input, please try again")


def create_season(season_years, handicap_formula, league_id):
    formula_as_json = json.dumps(handicap_formula)
    print(f"this is the json version of the token list: {handicap_formula}")
    new_season = Season(season_years=season_years, handicap_formula=formula_as_json, league_id=league_id)
    session = db_session.create_session()

    try:
        session.add(new_season)
        session.commit()
        league_name = new_season.league.league_name
        return new_season
    finally:
        session.close()



class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


