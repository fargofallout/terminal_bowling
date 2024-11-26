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
            print("huh?")
            continue

        match user_choice:
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid input, please try again")


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


