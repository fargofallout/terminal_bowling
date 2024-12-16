import regex
import sqlalchemy as sa

from data import db_session
from data.game import Game
from utils.utils import parse_global_options


def game_menu():
    return_to_main = False

    while not return_to_main:
        print("\ntemp")
        print("x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "x" | "X":
                return_to_main = True


