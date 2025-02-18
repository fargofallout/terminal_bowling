import regex

from utils.utils import parse_global_options, REqual
from utils.bowler_utils import create_bowler, modify_bowler, get_bowler_by_id, delete_bowler


def bowler_menu():
    return_to_main = False

    while not return_to_main:
        print("\n1 to add a new bowler")
        print("2 to modify a bowler")
        print("3 to delete a bowler")
        print("x to exit")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "1":
                print("enter user name in format firstname lastname")
                bowler_name = input(":").strip()
                name_regex = regex.search(r"^([^\n ]+) ([^\n ]+)$", bowler_name)
                if not name_regex:
                    print("inputted name is not in the correct format, please try again")
                    print("(look, I know this is not robust and you can't have a space in a last name,")
                    print("for instance, but I don't want to put a lot of effort into this part, so rather than")
                    print("having 'Von Hansen' as the last name, just make it 'VonHanen')")
                else:
                    first_name = name_regex.group(1)
                    last_name = name_regex.group(2)

                    new_bowler = create_bowler(first_name, last_name)
                    print(f"here's the new bowler: {new_bowler}")
            case "2":
                modify_bowler_menu()
            case "3":
                delete_bowler_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid choice, please try again")


def modify_bowler_menu():
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
            case r"^\w+ \w+$":
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
        print("\nenter the bowler's id to delete them")
        print("enter 'x' to return to the previous menu")
        print("and look, I'll expand this later and create something to search by name, but")
        print("I don't think I'm going to be doing a lot of deleting, so it isn't a priority right now")

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
                    print("that id wasn't found - please try again")
            case "x" | "X":
                return_to_modify_menu = True
            case _:
                print("invalid choice, please try again")

