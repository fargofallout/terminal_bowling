import regex

from utils.season_utils import get_season_by_id
from utils.team_utils import get_team_by_id
from utils.utils import parse_global_options, output_to_multiple_columns
from utils.bowler_utils import get_all_bowlers, get_bowler_by_id
from utils.head_to_head_utils import create_head_to_head


def create_new_week():
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
        print(f"left team: {teams[0]}")
        print(f"right team: {teams[1]}")

        # CONTINUE HERE: create the head-to-head, and then determine what's next - need to figure out
        # how to handle continuing a head-to-head that's in progress, and if everything from this point forward 
        # takes that into consideration
        all_bowlers = get_all_bowlers()
        output_to_multiple_columns(all_bowlers)

        print("\nabove is a list of all bowlers (hopefully with some team info eventually)")
        print("using those ids, enter the ids of all 10 (make this dynamic?) bowlers, separated by spaces")
        print("starting with the first bowler on the left lane, then the second, etc., going down the list")
        print("of bowlers on the left lane and then bowlers on the right lane")
        print("optionally, add a comman and a value for handiap after each bowler id, separated by spaces")
        print("for example, this is an input of 8 bolwer ids:")
        print("1 2 3 4 5 6 7 8")
        print("and this is an input for 8 bowlers with their handicaps:")
        print("1,10 2,50 3,22 4,30 5,0 6,11")

        bowler_list = get_bowler_ids()
        if not bowler_list:
            continue
        print(f"just making sure: {bowler_list}")

        new_head_to_head = create_head_to_head(new_week, teams[0].id, teams[1].id, the_season.id)
        if not new_head_to_head:
            print("not sure what went wrong, but something isn't cool")
            continue
        return new_head_to_head


def display_week(head_to_head, include_options=False):
    pass


def get_week():
    return_to_main = False

    while not return_to_main:
        print("\nthis is where I'd show you what the next week in this league is")
        print("but I can't really implement that until I have a week in the db,")
        print("so you can't actually hit enter at the next prompt and accomplish anything - just enter a number for a new week")

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


def get_bowler_ids():
    # TODO: if I wanted this to be flexible enough to accommodate leagues with different numbers of 
    # bowlers per team, I'd have to do some checking here, such as making sure the number of bowlers
    # entered divided by 2 equals the number per team specified in the league table
    return_to_prev_menu = False
    while not return_to_prev_menu:
        num_bowlers = 10
        print("\ninput the bowler ids here")
        bowler_ids = input(":").strip()

        if parse_global_options(bowler_ids):
            continue
        if bowler_ids in ["x", "X"]:
            return_to_prev_menu = True
            continue

        bowler_id_list = regex.split(r" +", bowler_ids)

        if len(bowler_id_list) != num_bowlers:
            print("you need to enter 10 bowler ids - please try again")
            continue

        has_invalid_entry = False
        return_list = []
        for each_id in bowler_id_list:
            id_handicap_split = each_id.split(",")

            if len(id_handicap_split) > 2:
                print(f"{each_id} is not a valid entry")
                has_invalid_entry = True
                continue

            the_bowler = get_bowler_by_id(id_handicap_split[0])
            if not the_bowler:
                has_invalid_entry = True
                print(f"{each_id} is not a valid id")

            if len(id_handicap_split) == 2 and not regex.search(r"^\d+$", id_handicap_split[1]):
                print(f"{id_handicap_split[1]} is not a valid handicap, please try again")
                has_invalid_entry = True
                continue

            return_list.append(id_handicap_split)

        if has_invalid_entry:
            continue

        else:
            return return_list


# def write_to_screen(**kwargs):
def write_to_screen(head_to_head_id=0):
    screen_width = 178

    characters_per_name = 23
    characters_per_handicap = 4
    characters_per_scratch_game = 4
    characters_per_handicap_game = 4
    characters_per_scratch_total = 5
    characters_per_handicap_total = 4
    characters_per_points = 3

    # this is dummy data
    left_lane_num = 31
    num_games = 3
    left_team = "big ern"
    right_team = "pin tillers"
    left_bowlers = [["christian schoeller", 30], ["tony hertzkowitz", 55], ["duke dancombe", 10], ["dana dancombe", 5], ["mike vacha", 50]]
    right_bowlers = [["jeff sis", 2], ["mike mingo", 3], ["rick aguliar", 10], ["bill vitt", 10], ["brian manchura", 0]]

    name_width = ((characters_per_name + 2) * 2) + 2
    hdcp_width = ((characters_per_handicap + 2) * 2) + 2
    games_width = characters_per_scratch_game + characters_per_handicap_game + 3 + num_games
    totals_width = 
    
    # CONTINUE HERE: ugh, am I overcomplicating this? I think I'm calculating for both halves in some cases, but 
    # only one half in other cases


    '''
    data to send:
    left lane number
    two team names
    num players per team? (do I need to be this flexible?)
    players/handicaps/scores
    num games per night?

    '''
    for num in range(screen_width):
        print("-", end="")

