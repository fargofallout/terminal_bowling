import regex
import sqlalchemy as sa

from data.bowler import Bowler
from data import db_session
from utils.utils import parse_global_options


def bowler_menu():
    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new bolwer") #done
        print("2 to modify a bowler") #done
        print("3 to delete a bowler") #done (but needs improvement)
        print("x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

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
                modify_bolwer_menu()
            case "3":
                delete_bowler_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid choice, please try again")


def modify_bolwer_menu():
    return_to_bowler_menu = False

    while not return_to_bowler_menu:
        print("\nenter the id of the bowler to modify")
        print("enter 'x' to exit")

        modify_input = input(":").strip()
        if parse_global_options(modify_input):
            continue

        match REqual(modify_input):
            case r"\d+":
                bowler_to_modify = get_bowler_by_id(int(modify_input))
                if bowler_to_modify:
                    get_new_name_menu(bowler_to_modify)
                    return_to_bowler_menu = True
                else:
                    print("that id wasn't found, please try again")
            case "x" | "X":
                return_to_bowler_menu = True
            case _:
                print("that's not a valid input")


def get_new_name_menu(bowler):
    return_to_modify_menu = False
    while not return_to_modify_menu:
        print("\n****************************")
        print(f"The bowler you'd like to modify is: {bowler}")
        print("****************************")
        print("enter the new name in the format 'firstname lastname'")
        print("enter 'x' to return to previous menu")

        user_choice = input(":").strip()

        match REqual(user_choice):
            case r"\w+ \w+":
                name_split = user_choice.split(" ")
                new_bowler_name = modify_bowler(bowler.id, name_split[0], name_split[1])
                if not new_bowler_name:
                    print("that bowler was not found, please try again")
                else:
                    print(f"new bowler name: {new_bowler_name.first_name} {new_bowler_name.last_name}")
                    return_to_modify_menu = True
            case "x" | "X":
                return_to_modify_menu = True
            case _:
                print("invalid choice")


def delete_bowler_menu():
    return_to_modify_menu = False

    while not return_to_modify_menu:
        print(f"\nenter the bowler's id to delete them")
        print(f"enter 'x' to return to the previous menu")
        print(f"and look, I'll expand this later and create something to search by name, but")
        print(f"I don't think I'm going to be doing a lot of deleting, so it isn't a priority right now")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match REqual(user_choice):
            case r"\d+":
                successful_deletion = delete_bowler(user_choice)
                if successful_deletion:
                    print("bowler has been deleted (this needs to be improved - add the name and whatnot)")
                    return_to_modify_menu = True
                else:
                    print(f"that id wasn't found - please try again")
            case "x" | "X":
                return_to_modify_menu = True
            case _:
                print("invalid choice, please try again")


def create_bowler(first_name, last_name):
    new_bolwer = Bowler(first_name=first_name, last_name=last_name)
    session = db_session.create_session()

    try:
        session.add(new_bolwer)
        session.commit()
        return f"{new_bolwer.id} {new_bolwer.first_name} {new_bolwer.last_name}"
    finally:
        session.close()


def delete_bowler(id):
    session = db_session.create_session()

    try:
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id==id)).one_or_none()
        if bowler:
            session.delete(bowler)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()


def get_bowler_by_id(id):
    session = db_session.create_session()
    try:
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id==id)).unique().one_or_none()
        # print(f"here's that bowler: {bowler}")
        # print(f"id? {bowler.id}")
        return bowler
    finally:
        session.close()


def modify_bowler(bowler_id, new_first_name, new_last_name):
    session = db_session.create_session()

    try:
        # session.execute(sa.update(Bowler),[{"id":bowler_id, "first_name": new_first_name, "last_name": new_last_name},],)
        bowler = session.scalars(sa.select(Bowler).where(Bowler.id == bowler_id)).one_or_none()
        if not bowler:
            return ""
        else:
            bowler.first_name = new_first_name
            bowler.last_name = new_last_name
            session.commit()
            return bowler

    finally:
        session.close()


#this idea is courtesy https://discuss.python.org/t/structural-pattern-matching-should-permit-regex-string-matches/22700/8
class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)


