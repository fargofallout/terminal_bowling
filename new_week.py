import regex

from utils.season_utils import get_season_by_id
from utils.utils import parse_global_options


def new_week_menu():
    return_to_main = False

    print("\n****************************")
    print("disclaimer: I have not included the ability to add teams or bowlers or")
    print("anything from this portion of the app, so if anything has to be added,")
    print("input 'x' at the next prompt to go back to the main menu and add whatever needs to be added")
    print("****************************")

    while not return_to_main:
        print("\n****************************")
        print("new week!")
        print("****************************")
        print("first, enter the id of the season")
        print("or enter 'x' to return to the main menu")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        if user_input.lower() == "x":
            return_to_main = True

        season_match = regex.search(r"^(\d+)$", user_input)
        if not season_match:
            print("please enter the id of a season")
            continue

        the_season = get_season_by_id(season_match.group(1))
        if not the_season:
            print("that is not a valid season id, please try again")
            continue

        print("\nthis is where I'd present what the next week in that league is")
        print("but I haven't implemented that yet and won't until I have a full week in the db?")

        print("\nto accept that week, simply hit enter at this prompt")
        print("otherwise, if it should be a different week for some reason, enter it here")

        user_input = input(":").strip()
        week_match = regex.search(r"^(\d+)$", user_input)
        if not user_input:
            print("I told you, this isn't implemented yet")
            continue

        elif week_match:
            new_week = int(week_match.group(1))
            print(f"new week will be week {new_week}")
            print("also, I need to make sure that week doesn't overlap with an existing week")
            print("ugh")

        else:
            print("that's not a valid input")
            continue

        print("\nnext, enter the two team ids with a space in between them")
        print("e.g., (I know this is obvious) 1 2")

        user_input = input(":").strip()
        # CONTINUE HERE
        print("should these all be separate menus like in the other utils files")
        print("so if there's a mistake in one, you don't have to do the whole thing over?")


