import regex
import sqlalchemy as sa

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

                    new_bowler = create_bowler(first_name, last_name)
                    print(f"here's the new bolwer: {new_bowler}")
            case "2":
                bowlers = get_all_bowlers()
                print("\nHere are all bowlers and their IDs:\n")
                for each_bowler in bowlers:
                    print(f"{each_bowler}")
            case "3":
                modify_bolwer_menu()
                
            case "x" | "X":
                return_to_main = True
            case _:
                print("you should choose 1 for now")
                return_to_main = True

def modify_bolwer_menu():

    #this idea is courtesy https://discuss.python.org/t/structural-pattern-matching-should-permit-regex-string-matches/22700/8
    class REqual(str):
        def __eq__(self, pattern):
            return regex.fullmatch(pattern, self)

    return_to_bowler_menu = False

    while not return_to_bowler_menu:
        print("\nenter the id of the bowler to modify")
        print("or enter 'L' to list all bowlers")
        print("enter 'x' to exit")
        modify_input = input(":").strip()

        match REqual(modify_input):
            case "l" | "L":
                # probably need to format this more nicely so it's across multiple columns
                all_bowlers = get_all_bowlers()
                for each_bowler in all_bowlers:
                    print(each_bowler)
            case r"\d+":
                user_to_modify = get_bowler_by_id(int(modify_input))
                if user_to_modify:
                    get_new_name_menu(user_to_modify)
                else:
                    print("that id wasn't found, please try again")
            case "x" | "X":
                return_to_bowler_menu = True
            case _:
                print("that's not a valid input")


def get_new_name_menu(bowler):
    #this idea is courtesy https://discuss.python.org/t/structural-pattern-matching-should-permit-regex-string-matches/22700/8
    class REqual(str):
        def __eq__(self, pattern):
            return regex.fullmatch(pattern, self)

    return_to_modify_menu = False

    while not return_to_modify_menu:
        print(f"\nThe bowler being modified is {bowler}")
        print("enter the new name in the format 'firstname lastname'")
        print("enter 'x' to return to previous menu")
        user_choice = input(":").strip()

        match REqual(user_choice):
            case r"\w+ \w+":
                print("that's a valid name and I would presumably change this bowler to that?")
            case "x" | "X":
                return_to_modify_menu = True
            case _:
                print("invalid choice")


def create_bowler(first_name, last_name):
    new_bolwer = Bowler(first_name=first_name, last_name=last_name)
    session = db_session.create_session()

    try:
        session.add(new_bolwer)
        session.commit()
        return f"{new_bolwer.id} {new_bolwer.first_name} {new_bolwer.last_name}"
    finally:
        session.close()


def get_bowler_by_id(id):
    session = db_session.create_session()
    try:
        user = session.scalars(sa.select(Bowler).where(Bowler.id==id)).one_or_none()
        # print(f"here's that user: {user}")
        # print(f"id? {user.id}")
        return user
    finally:
        session.close()


def get_all_bowlers():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Bowler).order_by(Bowler.id)).all()
        return result
    finally:
        session.close()

def modify_bowler(bowler_id, new_first_name, new_last_name):
    pass

