import sqlalchemy as sa
from pathlib import Path

import data.db_session as db_session


def configure_db():

    file = (Path(__file__).parent / "db" / "db.sqlite")
    db_session.global_init(file)

def main():

    exit_prog = False

    while not exit_prog:
        # print(f"is this this current file? {__file__}")
        # print(f"I assume this is the full path: {Path(__file__).parent}")
        print("1 to begin a new week")
        print("2 for player menu")
        print("3 for team menu")
        print("4 for league menu")
        print("5 for alley menu")
        print(f"x to exit\n")

        user_choice = input(":").strip()

        # print(f"entered {user_choice}")

        match user_choice:
            case "1":
                print("doing 1 stuff")
            case "2":
                print("doing 2 stuff")
            case "3":
                print("doing 3 stuff")
            case "4":
                print("doing 4 stuff")
            case "5":
                print("doing 5 stuff")
            case "x" | "X":
                exit_prog = True
            case _:
                print("not a valid input")

if __name__ == "__main__":
    main()
else:
    print("when would I ever hit this?")

