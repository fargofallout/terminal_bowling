import regex
import json

from utils.utils import parse_global_options, REqual, parse_formula, recursive_calc_function
from utils.season_utils import create_season, delete_season, get_season_by_id, update_season
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
            case "3":
                delete_season_menu()
            case _:
                print("not a valid input, please try again")


def new_season_menu():
    return_to_season_menu = False
    while not return_to_season_menu:
        print("\n***********************************************")
        print("note: a season has to be attached to a league")
        print("enter a season in this format:")
        print("***********************************************")
        print("league_id [season_timeframe] (handicap_formula) games_per_week players_per_team")
        print("e.g., 1 [2024-2025] ((220 - average) * 0.9) 3 5")
        print("***********************************************")
        print("for the formula, make sure to wrap each pair of values in parentheses")
        print("such as (230 - (average * .8))     rather than      (230 - average * .8)")
        print("only one unique variable is allowed - if it ever becomes necessary to expand that, I'll figure it out")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        match REqual(user_input):
            case "x" | "X":
                return_to_season_menu = True
            # user input is in this format: 1 [timeframe] (formula)
            case r"^(\d+) +\[([^\n\[\]]+)\] +(\([^\n]+\)) +(\d+) +(\d+)$":
                season_match = regex.search(r"^(\d+) +\[([^\n\[\]]+)\] +(\([^\n]+\)) +(\d+) +(\d+)$", user_input)
                league_id = season_match.group(1)
                season_timeframe = season_match.group(2)
                handicap_formula = season_match.group(3)
                games_per_week = season_match.group(4)
                players_per_team = season_match.group(5)
                league = get_league_by_id(league_id)
                if not league:
                    print(f"not a valid league id, please try again - here's the league id: {league_id}")
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
                        new_season = create_season(season_timeframe, token_list, league_id, games_per_week, players_per_team)
                        print(f"{new_season}")

            case _:
                print("that's not a valid input, please try again")


def modify_season_menu():
    return_to_season_menu = False
    while not return_to_season_menu:
        print("\n********************************")
        print("enter the season modification in this format: season_id modifcation_choice (new_value)")
        print("e.g., 1 2 ((215 - average) * 0.90)")
        print("or 2 1 (2024-2025)")
        print("********************************")
        print("1 for season timeframe")
        print("2 for handicap formula")
        print("3 for the season's related league")
        print("4 for number of games per week")
        print("5 for number of bowlers per team")

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
            case r"^(\d+) +1 +\(([^\n]+)\)$":
                season_timeframe_match = regex.search(r"^(\d+) +1 +\(([^\n]+)\)$", season_input)
                new_timeframe = season_timeframe_match.group(2)
                updated_season = update_season(season_id, season_timeframe=new_timeframe)
                print(f"updated season: {updated_season}")
                return_to_season_menu = True

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
                return_to_season_menu = True

            case r"^(\d+) +3 +\((\d+)\)$":
                new_season_match = regex.search(r"^(\d+) +3 +\((\d+)\)$", season_input)
                season_id = new_season_match.group(1)
                new_league_id = new_season_match.group(2)

                new_league = get_league_by_id(new_league_id)
                if not new_league:
                    print("that league doesn't exist, please try again")
                    continue
                updated_season = update_season(season_id, league_id=new_league_id)
                if not updated_season:
                    print("like with leagues, I don't know how this could go wrong - I guess try again?")
                    continue
                actual_updated_season = get_season_by_id(season_id)
                print(f"updated season: {actual_updated_season}")
                return_to_season_menu = True

            case r"^(\d+) +4 +\((\d+)\)$":
                mod_season_match = regex.search(r"^(\d+) +4 +\((\d+)\)$", season_input)
                games_per_week = int(mod_season_match.group(2))
                updated_season = update_season(season_id, games_per_week=games_per_week)
                if not updated_season:
                    print("not sure what went wrong here")
                    continue
                actual_updated_season = get_season_by_id(season_id)
                print(f"updated season: {actual_updated_season}")
                return_to_season_menu = True

            case r"^(\d+) +5 +\((\d+)\)$":
                mod_season_match = regex.search(r"^(\d+) +5 +\((\d+)\)$", season_input)
                players_per_team = int(mod_season_match.group(2))
                updated_season = update_season(season_id, players_per_team=players_per_team)
                if not updated_season:
                    print("season wasn't updtaed and I don't know why")
                    continue
                actual_updated_season = get_season_by_id(season_id)
                print(f"updated season: {actual_updated_season}")
                return_to_season_menu = True

            case "x" | "X":
                return_to_season_menu = True
            case _:
                print("not a valid input, please try again")


def delete_season_menu():
    return_to_season_menu = False

    while not return_to_season_menu:
        print("\nplease enter the id of the season to delete")
        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        input_match = regex.search(r"^(\d+)$", user_input)
        if user_input in ["x", "X"]:
            return_to_season_menu = True
        elif input_match:
            season_id = input_match.group(1)
            this_season = get_season_by_id(season_id)
            if not this_season:
                print("that id doesn't exist, please try again")
                continue

            successful_deletion = delete_season(input_match.group(1))
            if successful_deletion:
                print("the season deletion was successful")
                return_to_season_menu = True
            else:
                print("something went wrong with the deletion, please try again")

        else:
            print("that is not a valid input, please try again")

