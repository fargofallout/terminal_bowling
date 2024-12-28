import regex
import sqlalchemy as sa

from data import db_session
from data.game import Game
from utils.utils import parse_global_options


def game_menu():
    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new game")
        print("2 to modify a game")
        print("3 to delete a game")
        print("x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_chhoice:
            case "1":
                add_game_menu()
            case "x" | "X":
                return_to_main = True

def add_game_menu():
    return_to_game_menu = False

    while not return_to_game_menu:
        print("\nenter the new game in this format:")
        print("bowler_id game_score handicap game_number")
        print("e.g., 5 188 45 3")

        # continue here
        match REqual(r"^"):

class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)

