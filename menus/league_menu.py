import regex

from utils.league_utils import create_league, modify_league, get_league_by_id, delete_league
from utils.alley_utils import get_alley_by_id
from utils.utils import parse_global_options, REqual


def league_menu():
    return_to_main = False
    while not return_to_main:
        # TODO: need to add the option to delete leagues
        print("\n****************************")
        print("NOTE: you will need to associate an alley with this league to be able to create it")
        print("****************************")
        print("1 to add a new league")
        print("2 to modify an existing league")
        print("3 to delete a league")
        print("'x' to return to main menu")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match user_choice:
            case "1":
                create_league_menu()
            case "2":
                modify_league_menu()
            case "3":
                delete_league_menu()
            case "x" | "X":
                return_to_main = True
            case _:
                print("not a valid input, please try again")


def create_league_menu():
    return_to_league_menu = False
    while not return_to_league_menu:
        print("\nenter alley id and league name in this format:")
        print("1 flaherty's tuesday nights")
        print("or 'x' to return to the main league menu")

        league_input = input(":").strip()
        if parse_global_options(league_input):
            continue

        match REqual(league_input):
            case "x" | "X":
                return_to_league_menu = True
            case r"^(\d+) +([^\n]+)$":
                league_match = regex.search(r"^(\d+) +([^\n]+)$", league_input)
                alley_id = league_match.group(1)
                league_name = league_match.group(2)
                print(f"alley: {alley_id}, league: {league_name}")
                alley = get_alley_by_id(alley_id)
                if not alley:
                    print("alley id does not exist, please try again")
                    continue
                new_league = create_league(league_name, alley_id)
                print(f"new league: {new_league}")
                return_to_league_menu = True
            case _:
                print("not a valid input, please try again")


def modify_league_menu():
    return_to_league_menu = False
    while not return_to_league_menu:
        # TODO: I don't like how this looks in the terminal
        print("\n*************************************************")
        print("to modify a league, use the format 'ml league_id new_leauge_name', e.g.,")
        print("ml 5 new league name")
        print("*************************************************")
        print("to modify the alley associated with a league, use the format 'ma league_id new_alley_id', e.g.,")
        print("ma 5 10")
        print("*************************************************")

        league_input = input(":").strip()
        if parse_global_options(league_input):
            continue

        match REqual(league_input):
            case "x" | "X":
                return_to_league_menu = True

            case r"^ml +(\d+) +([^\n]+)$":
                modify_league_match = regex.search(r"^ml +(\d+) +([^\n]+)$", league_input)
                league_id = modify_league_match.group(1)
                new_league_name = modify_league_match.group(2)
                league = get_league_by_id(league_id)
                if not league:
                    print("that league does not exist, please try again")
                    continue
                new_league = modify_league(league_id, new_name=new_league_name)
                if not new_league:
                    print("dammit, something went wrong changing the league name")
                return_to_league_menu = True

            case r"^ma +(\d+) +(\d+)$":
                modify_alley_match = regex.search(r"^ma +(\d+) +(\d+)$", league_input)
                league_id = modify_alley_match.group(1)
                new_alley_id = modify_alley_match.group(2)
                league = get_league_by_id(league_id)
                alley = get_alley_by_id(new_alley_id)
                if not league:
                    print("that league id is not valid, please try again")
                    continue
                if not alley:
                    print("that alley id is not valid, please try again")
                    continue
                new_league = modify_league(league_id, new_alley_id=new_alley_id)
                if not new_league:
                    print("dammit, not sure what could have went wrong with changing the league's alley")
                    continue
                actual_new_league = get_league_by_id(league_id)
                print(f"updated league info: {actual_new_league}")
                return_to_league_menu = True

            case _:
                print("not a valid input, please try again")


def delete_league_menu():
    return_to_league_menu = False
    while not return_to_league_menu:
        print("\nenter the league's id to delete it")
        print("or 'x' to return to the previous menu")

        user_choice = input(":").strip()
        if parse_global_options(user_choice):
            continue

        match REqual(user_choice):
            case r"^\d+$":
                successful_deletion = delete_league(user_choice)
                if successful_deletion:
                    print("league has been deleted")
                    return_to_league_menu = True
                else:
                    print("league wasn't found, please try again")

            case "x" | "X":
                return_to_league_menu = True

            case _:
                print("not a valid input, please try again")

