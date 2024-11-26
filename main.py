import sqlalchemy as sa
from pathlib import Path

import data.db_session as db_session
from utils import bowler_utils, team_utils, alley_utils, league_utils, season_utils
from utils.utils import parse_global_options


def configure_db():

    file = (Path(__file__).parent / "db" / "db.sqlite")
    db_session.global_init(file.as_posix())
    # print(f"what if it's file as posix? {file.as_posix()}, {type(file.as_posix())}")

def main():
    configure_db()

    print("\n********************")
    print("in almost all menus, enter b to list all bowlers, t to list all teams,")
    print("l to list all leagues, a to list all alleys, and s to list all seasons")
    print("and h for help?")
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
        print(f"x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        # print(f"entered {user_choice}")

        match user_choice:
            case "1":
                print("doing 1 stuff")
            case "2":
                bowler_utils.bowler_menu()
            case "3":
                team_utils.team_menu()
            case "4":
                league_utils.league_menu()
            case "5":
                alley_utils.alley_menu()
            case "6":
                season_utils.season_menu()
            case "x" | "X":
                exit_prog = True
            case _:
                print("not a valid input")

if __name__ == "__main__":
    main()
else:
    print("when would I ever hit this?")

