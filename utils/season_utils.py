import regex
import sqlalchemy as sa

from data import db_session
from data.season import Season
from utils.utils import parse_global_options


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
            case _:
                print("not a valid input, please try again")
                # CONTINUE HERE: need to add seaons and whatnot


def new_season_menu():
    return_to_season_menu = False
    while not return_to_season_menu:
        print("\n************")
        print("note: a season has to be attached to a league")
        print("enter a season in the format [league id] [season timeframe] [handicap formula]")
        print("example:")
        print("1 [2024-2025] ((220 - average) * 0.9)")
        print("notes: put the season timeframe in square brackets and the formula in parentheses")
        print("for the formula, make sure to wrap each pair of values in parentheses")
        print("I'm omly accepting 'average' as a variable for now, but if I encounter something else, I'll deal with it")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        match REqual(user_input):
            case "x" | "X":
                return_to_season_menu = True
            case r"^(\d+) +\[([^\n\[\]]+)\] +\(([^\n]+)\)$":
                print("that appears to be a valid input")
                season_match = regex.search("^(\d+) +\[([^\n\[\]]+)\] +\(([^\n]+)\)$", user_input)
                print(f"id: {season_match.group(1)}, season: {season_match.group(2)}, formula: {season_match.group(3)}")
            case _:
                print("that's not a valid input, please try again")


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


