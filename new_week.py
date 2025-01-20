import regex

from utils.season_utils import get_season_by_id
from utils.team_utils import get_team_by_id
from utils.utils import parse_global_options
from utils.bowler_utils import get_all_bowlers


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

        new_week = get_week()
        if not new_week:
            continue
        print(f"got {new_week} for the week")

        teams = get_teams()
        if not teams:
            continue
        print(f"this is team 1: {teams[0]}")
        print(f"this is team 2: {teams[1]}")

        all_bowlers = get_all_bowlers()
        for each_bowler in all_bowlers:
            print(each_bowler)
        # CONTINUE HERE: need to provide a list of bowler next and get an input for all of them
        # this is where things get complicated - I should have bowler associated with a team in some way,
        # but I think that should be based on them having bowled with a team and not actually have there be a 
        # foreign key relationship between bowler/team


def get_week():
    return_to_main = False

    while not return_to_main:
        print("\nthis is where I'd show you what the next week in this league is")
        print("but I can't really implement that until I have a week in the db,")
        print("so you can't actually hit enter at the next prompt and accomplish anything - just enter a nmber for a new week")

        print("\nto accept that week, just press 'enter'")
        print("otherwise, enter the week number here to input data for a specific week")

        week_input = input(":").strip()
        if parse_global_options(week_input):
            continue

        if week_input in ["x", "X"]:
            return_to_main = True
            return ""

        week_match = regex.search(r"^(\d+)$", week_input)
        if not week_input:
            print("I told you, this isn't implemented yet")
            continue

        elif week_match:
            new_week = int(week_match.group(1))
            # TODO: see below
            print("also, I need to make sure that week doesn't overlap with an existing week")
            print("ugh")

            return new_week

        else:
            print("not a valid input, please try again")
            continue


def get_teams():
    return_to_main = False
    while not return_to_main:
        print("\nnext, enter the team ids in the format left_team_id right_team_id")
        print("e.g., (I know this is obvious) 1 2")

        user_input = input(":").strip()
        if parse_global_options(user_input):
            continue

        if user_input in ["x", "X"] or not user_input:
            return_to_main = True
            return

        teams_match = regex.search(r"^(\d+) +(\d+)$", user_input)
        if not teams_match:
            print("that is not a valid input, please try again")
            continue

        team_one_id = int(teams_match.group(1))
        team_one = get_team_by_id(team_one_id)
        team_two_id = int(teams_match.group(2))
        team_two = get_team_by_id(team_two_id)

        if not team_one and not team_two:
            print("neither team id is valid, please try again")
            continue
        elif not team_one:
            print("team one is not valid, please try again")
            continue
        elif not team_two:
            print("team two is not valid, please try agian")
            continue
        elif team_one_id == team_two_id:
            print("you can't have the same team on both sides, please try again")
            continue

        print("I guess they're valid?")
        return team_one, team_two

