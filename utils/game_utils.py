import regex
import sqlalchemy as sa

from data import db_session
from data.game import Game
from utils.utils import parse_global_options
from utils.bowler_utils import get_bowler_by_id


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

        match user_choice:
            case "1":
                add_game_menu()
            case "2":
                modify_game_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid input, please try again")


def add_game_menu():
    return_to_game_menu = False

    while not return_to_game_menu:
        print("\nenter the new game in this format:")
        print("bowler_id game_score handicap game_number")
        print("e.g., 5 188 45 3")

        user_game = input(":").strip()
        if parse_global_options(user_game):
            continue

        match REqual(user_game):
            case r"^(\d+) +(\d+) +(\d+) +(\d+)$":
                score_match = regex.search(r"^(\d+) +(\d+) +(\d+) +(\d+)$", user_game)
                bowler_id = int(score_match.group(1))
                game_score = int(score_match.group(2))
                game_handicap = int(score_match.group(3))
                game_number = int(score_match.group(4))

                bowler = get_bowler_by_id(bowler_id)
                if not bowler:
                    print("bowler id is not valid, please try again")
                    continue

                new_game = create_game(game_score, game_handicap, game_number, bowler_id)
                print(f"here is the new game: {new_game}")

                return_to_game_menu = True

            case "x" | "X":
                return_to_game_menu = True

            case _:
                print("not a valid input, please try again")


def modify_game_menu():
    return_to_game_menu = False

    while not return_to_game_menu:
        print("\nenter the game to modify in this format:")
        print("game_id bowler_id game_score handicap game_number")
        print("for any values not being modified, use an underscore in that position")
        print("e.g., if only changing the score of a game, the input would be")
        print("1 _ 210 _ _")

        user_game = input(":").strip()
        if parse_global_options(user_game):
            continue

        match REqual(user_game):
            case r"^(\d+) +(\d+|_) +(\d+|_) +(\d+|_) +(\d+|_)$":
                game_match = regex.search(r"^(\d+) +(\d+|_) +(\d+|_) +(\d+|_) +(\d+|_)$", user_game)
                game_id = int(game_match.group(1))
                bowler_id = game_match.group(2)
                if bowler_id != "_":
                    bolwer = get_bowler_by_id(bowler_id)
                    if not bolwer:
                        print("that bowler doesn't exist?")
                        continue
                score = game_match.group(3)
                handicap = game_match.group(4)
                game_number = game_match.group(5)
                updated_game = modify_game(game_id, bowler_id=bowler_id, score=score, handicap=handicap, game_number=game_number)
                if updated_game:
                    print(f"here is the your updated game: {updated_game}")
                    # CONTINUE HERE:
                    # apparently sqlite doesn't care about types and I need to make sure I'm using the correct
                    # type when I insert them - I need to go through and update some types in my creation/updating functions
                else:
                    print("something went wrong, try again")
            case "x" | "X":
                return_to_game_menu = True

            case _:
                print("not a valid input, please try again")


def create_game(score, handicap, game_number, bowler_id):
    new_game = Game(score=score, handicap=handicap, game_number=game_number, bowler_id=bowler_id)
    session = db_session.create_session()

    try:
        session.add(new_game)
        session.commit()
        return new_game
    finally:
        session.close()


def modify_game(game_id, bowler_id=None, score=None, handicap=None, game_number=None):
    session = db_session.create_session()

    try:
        game = session.scalars(sa.select(Game).where(Game.id == game_id)).unique().one_or_none()
        if not game:
            return ""
        else:
            if bowler_id != "_":
                game.bowler_id = int(bowler_id)
            if score != "_" and score.isdigit():
                game.score = int(score)
            session.commit()
            return game

    finally:
        session.close()



class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


