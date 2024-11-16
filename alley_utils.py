import regex
import sqlalchemy as sa

from data import db_session
from data.alley import Alley


def alley_menu():

    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new alley")
        print("2 to list all alleys")
        print("3 to modify an existing alley")
        print("press x to return to main menu")

        user_choice = input(":").strip()

        match user_choice:
            case "1":
                print("enter the alley name")
                print("and, optionally, the city name in parentheses")
                alley_input = input(":").strip()
                alley_regex = regex.search(r"([^\n\(\)]+) *(?:\(([^\n\(\)]+)\))?", alley_input)
                if alley_regex:
                    alley_name = alley_regex.group(1).strip()
                    alley_city = alley_regex.group(2).strip()
                    new_alley = add_alley(alley_name, alley_city)
                    print(f"{new_alley} has been created")
                else:
                    print("not even sure how I managed, but that alley name doesn't work - try again")

            case "2":
                all_alleys = get_all_alleys()
                print("****************************")
                for each_alley in all_alleys:
                    print(each_alley)
                print("****************************")
            case "3":
                modify_alley_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid option - please try again")


def modify_alley_menu():
    class REqual(str):
        def __eq__(self, pattern):
            return regex.fullmatch(pattern, self)

    return_to_alley_menu = False
    while not return_to_alley_menu:
        print("\nenter 'l' to list all alleys")
        print("enter alley's id you would like to modify")
        print("enter 'x' to return to main alley menu")

        user_input = input(":").strip()

        match REqual(user_input):
            case "l" | "L":
                all_alleys = get_all_alleys()
                print("****************************")
                for each_alley in all_alleys:
                    print(each_alley)
                print("****************************")
            case "x" | "X":
                return_to_alley_menu = True
            case r"\d+":
                get_alley_or_city_menu()
            case _:
                print("not a valid input, please try again")


def get_alley_or_city_menu():
    return_to_modification_menu = False

    while not return_to_modification_menu:
        print("good lord, this is a lot of menuing")
        print("enter 'x' to return to the previous menu")

        user_input = input(":").strip()

        match user_input:
            case "x" | "X":
                return_to_modification_menu = True
            case _:
                print("yeah, I have to do stuff here")


def add_alley(alley_name, city_name=None):
    new_alley = Alley(alley_name=alley_name, alley_city=city_name)
    session = db_session.create_session()

    try:
        session.add(new_alley)
        session.commit()
        return new_alley
    finally:
        session.close()


def modify_alley_name(alley_id, new_name):
    session = db_session.create_session()
    try:
        alley = session.scalars(sa.select(Alley).where(Alley.id==alley_id)).one_or_none()
        if not alley:
            return ""
        else:
            alley.alley_name = new_name
            session.commit()
            return alley
    finally:
        session.close()


def get_all_alleys():
    session = db_session.create_session()
    try:
        all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).all()
        return all_alleys
    finally:
        session.close()

