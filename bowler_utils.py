import regex

from data.bowler import Bowler
from data import db_session


def bowler_menu():
    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new bolwer")
        print("2 to list all bowlers")
        print("3 to modify a bowler")
        print("4 to delete a bowler")
        print("x to exit")

        user_choice = input(":").strip()

        match user_choice:
            case "1":
                print("enter user name in format firstname lastname")
                bowler_name = input(":").strip()
                name_regex = regex.search(r"(\w+) (\w+)", bowler_name)
                if not name_regex:
                    print("inputted name is not in the correct format, please try again")
                else:
                    first_name = name_regex.group(1)
                    last_name = name_regex.group(2)

                    create_bowler(first_name, last_name)
                    print("was that successful?")
            case "x":
                return_to_main = True
            case _:
                print("you should choose 1 for now")
                return_to_main = True

def create_bowler(first_name, last_name):
    new_bolwer = Bowler(first_name=first_name, last_name=last_name)
    session = db_session.create_session()

    try:
        session.add(new_bolwer)
        session.commit()
    finally:
        session.close()


def get_all_bowlers():
    pass

