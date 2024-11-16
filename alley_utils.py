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
                print("listing all alleys")
            case "3":
                print("modifying an alley")
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid option - please try again")


def add_alley(alley_name, city_name=None):
    new_alley = Alley(alley_name=alley_name, alley_city=city_name)
    session = db_session.create_session()

    try:
        session.add(new_alley)
        session.commit()
        return new_alley
    finally:
        session.close()


