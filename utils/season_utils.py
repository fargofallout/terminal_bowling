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
            case r"^(\d+) +\[([^\n\[\]]+)\] +(\([^\n]+\))$":
                season_match = regex.search("^(\d+) +\[([^\n\[\]]+)\] +(\([^\n]+\))$", user_input)
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
        print("\nenter the season modification in this format: [league id] [modifcation choice] [(new value)]")
        print("e.g., 1 2 ((215 - average) * 0.90)")
        print("or 2 1 (2024-2025)")
        print("modification choices are 1 for the season timefram, 2 for the handicap formula, and 3 for the season's league")

        season_input = input(":").strip()
        if parse_global_options(season_input):
            continue

        season_id_regex = regex.search(r"^(\d+)", season_input)
        if season_id_regex:
            season_id = season_id_regex.group(1)
            season = get_season_by_id(season_id)
            if not season:
                print("that season id doesn't match, please try again")
                continue

        match REqual(season_input):
            case r"^(\d+) +1 +(\([^\n]+\))$":
                season_timeframe_match = regex.search(r"^(\d+) +1 +(\([^\n]+\))$", season_input)
                new_timeframe = season_timeframe_match.group(2)
                updated_season = update_season(season_id, season_timeframe=new_timeframe)
                print(f"updated season: {updated_season}")

            case r"^(\d+) +2 +(\([^\n]+\))$":
                season_formula_match = regex.search(r"^(\d+) +2 +(\([^\n]+\))$", season_input)
                season_id = season_formula_match.group(1)
                new_formula = season_formula_match.group(2)
                token_list = parse_formula(new_formula)
                if not token_list:
                    print("there was a problem with the formula (hopefully it has already been printed), please try again")
                    continue
                print("new formula has passed the initial check, enter a sample average (just an integer to make my life easier) to see what value it spits out")
                sample_average = input(":").strip()
                if not regex.search(r"^\d+$", sample_average):
                    print("\nthat not a valid number, and look, I'm not going to go through the effort of letting you try entering an average again, because")
                    print("that's some unnecessary work - you have to re-enter the formula and then try a sample average again")
                    continue
                sample_handicap = recursive_calc_function(token_list, int(sample_average))
                print(f"\nyour average of {sample_average} returned a handicap of {sample_handicap} and has been set")
                print("if it needs to be changed, you'll need to repeat this workflow of setting the formula")
                json_token_list = json.dumps(token_list)
                updated_season = update_season(season_id, handicap_formula=json_token_list)
                print(f"here is your new season: {updated_season}")
            case r"^(\d+) +3 +\(\d+\)$":
                # CONTINUE HERE: updating the season's league number
                print("modifying the league")
            case "x" | "X":
                return_to_season_menu = True
            case _:
                print("not a valid input, please try again")



def create_season(season_years, handicap_formula, league_id):
    # TODO: should I do this here, or should I do it before calling the function? I should probably do it before calling it, right? 
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


def get_season_by_id(season_id):
    session = db_session.create_session()
    try:
        season = session.scalars(sa.select(Season).where(Season.id==season_id)).one_or_none()
        return season
    finally:
        session.close()


def update_season(season_id, season_timeframe=None, handicap_formula=None, league_id=None):
    session = db_session.create_session()
    try:
        season = session.scalars(sa.select(Season).where(Season.id==season_id)).one_or_none()
        if season_timeframe:
            season.season_years = season_timeframe
            session.commit()
            return season
        elif handicap_formula:
            season.handicap_formula = handicap_formula
            session.commit()
            return season
    finally:
        session.close()

class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


