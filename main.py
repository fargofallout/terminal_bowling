# import sqlalchemy as sa
from pathlib import Path

import data.db_session as db_session
from utils.utils import parse_global_options
from new_week import new_week_menu
from menus import team_menu, bowler_menu, alley_menu, league_menu, season_menu, game_menu


def configure_db():

    file = (Path(__file__).parent / "db" / "db.sqlite")
    db_session.global_init(file.as_posix())
    # print(f"what if it's file as posix? {file.as_posix()}, {type(file.as_posix())}")


def main():
    configure_db()

    print("\n********************")
    print("in almost all menus, enter b to list all bowlers, t to list all teams,")
    print("l to list all leagues, a to list all alleys, s to list all seasons,")
    print("g to list all games, and h for help?")
    print("********************")

    exit_prog = False

    while not exit_prog:
        # print(f"is this this current file? {__file__}")
        # print(f"I assume this is the full path: {Path(__file__).parent}")
        print("\n1 to begin a new week")
        print("2 for bowler menu")
        print("3 for team menu")
        print("4 for league menu")
        print("5 for alley menu")
        print("6 for season menu")
        print("7 for game menu (probably only for my games outside of a head-to-head?)")
        print("x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        # print(f"entered {user_choice}")

        match user_choice:
            case "1":
                new_week_menu()
            case "2":
                bowler_menu.bowler_menu()
            case "3":
                team_menu.team_menu()
            case "4":
                league_menu.league_menu()
            case "5":
                alley_menu.alley_menu()
            case "6":
                season_menu.season_menu()
            case "7":
                game_menu.game_menu()
            case "x" | "X":
                exit_prog = True
            case _:
                print("not a valid input")


if __name__ == "__main__":
    main()
else:
    print("when would I ever hit this?")

