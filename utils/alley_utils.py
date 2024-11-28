import regex
import sqlalchemy as sa

from data import db_session
from data.alley import Alley
from utils.utils import parse_global_options


def alley_menu():

    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new alley")
        print("2 to modify an existing alley")
        print("press x to return to main menu")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "1":
                print("\nenter the alley name")
                print("and, optionally, the city name in parentheses")
                print("e.g., flaherty's arden bowl (roseville)")
                alley_input = input(":").strip()
                alley_regex = regex.search(r"([^\n\(\)]+)(?: *\(([^\n\(\)]+)\))?", alley_input)
                if alley_regex:
                    alley_name = alley_regex.group(1).strip()
                    alley_city = alley_regex.group(2)
                    print(f"what is this? {alley_city}")
                    if alley_city:
                        alley_city = alley_city.strip()
                    new_alley = add_alley(alley_name, alley_city)
                    print(f"{new_alley} has been created")
                else:
                    print("not even sure how I managed, but that alley name doesn't work - try again")
            case "2":
                modbfy_alley_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid option - please try again")


def modify_alley_menu():
    return_to_alley_menu = False
    while not return_to_alley_menu:
        print("\nenter alley's id you would like to modify")
        print("enter 'x' to return to main alley menu")

        user_input = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match REqual(user_input):
            case "x" | "X":
                return_to_alley_menu = True
            case r"\d+":
                alley = get_alley_by_id(user_input)
                if alley:
                    get_alley_or_city_menu(alley)
                else:
                    print("not a valid id, please try again")
            case _:
                print("not a valid input, please try again")


def get_alley_or_city_menu(alley):
    return_to_modification_menu = False
    while not return_to_modification_menu:
        print("\n****************************")
        print(f"the alley you're modifying is {alley}")
        print("****************************")

        print("enter 1 followed by the new alley name to change just the alley name")
        print("enter 2 followed by the city name to change just the city name")
        print("enter 3 followed by the alley name and the city name in parentheses to change both")
        print("e.g., 3 flaherty's (roseville)")
        print("enter 'x' to return to the previous menu")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        match REqual(user_input):
            case "x" | "X":
                return_to_modification_menu = True
            case r"1 +([^\n]+)":
                one_match = regex.search(r"1 +([^\n]+)", user_input)
                modified_alley = modify_alley(alley.id, new_name=one_match.group(1))
                print(f"\nnew alley: {modified_alley}\n")
                return_to_modification_menu = True
            case r"2 +([^\n]+)":
                two_match = regex.search(r"2 +([^\n]+)", user_input)
                modified_alley = modify_alley(alley.id, new_city=two_match.group(1))
                print(f"\nnew alley: {modified_alley}\n")
                return_to_modification_menu = True
            case r"3 +([^\n]+) +\(([^\n\(\)]+)\)":
                three_match = regex.search(r"3 +([^\n]+) +\(([^\n\(\)]+)\)", user_input)
                modified_alley = modify_alley(alley.id, new_name=three_match.group(1), new_city=three_match.group(2))
                print(f"\nnew alley: {modified_alley}\n")
                return_to_modification_menu = True
            case _:
                print("that's an invalid entry, please try again")


def add_alley(alley_name, city_name=None):
    new_alley = Alley(alley_name=alley_name, alley_city=city_name)
    session = db_session.create_session()

    try:
        session.add(new_alley)
        session.commit()
        return new_alley
    finally:
        session.close()


def modify_alley(alley_id, new_name=None, new_city=None):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id==alley_id)).one_or_none()
        if not alley:
            return ""
        else:
            if new_name and not new_city:
                alley.alley_name = new_name
            elif new_city and not new_name:
                alley.alley_city = new_city
            else:
                alley.alley_name = new_name
                alley.alley_city = new_city
            session.commit()
            return alley
    finally:
        session.close()


def get_alley_by_id(alley_id):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id==alley_id)).one_or_none()
        return alley
    finally:
        session.close()


class REqual(str):
    def __eq__(self, pattern):
        return regex.fullmatch(pattern, self, regex.IGNORECASE)

