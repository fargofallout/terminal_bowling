import regex

from utils.season_utils import get_season_by_id
from utils.team_utils import get_team_by_id
from utils.utils import parse_global_options, output_to_multiple_columns
from utils.bowler_utils import get_all_bowlers, get_bowler_by_id
from utils.head_to_head_utils import create_head_to_head


def new_week_loop(head_to_head):
    # continue here: been so long since I worked on this, I forgot what I was thinking
    # once the head_to_head has been created, the next step is to display it, which I was working on,
    # but this loop needs to handle giving the display function information to display, and I forgot I had
    # created the user_action_numbers table - I think it makes sense to create a fuction where 
    # the action numbers are generated and given back to this function, and then.....I don't know for sure
    # ---- send something like {"teams": [[1, big ern], [2, bogarts]], "bowlers": [[4, tony], [5, christian]]}, etc.
    # maybe split those into right and left, and make them lists of dicts or something
    # the numbers there would correspond to action_number in the action numbers table
    # so when a number is entered, a lookup is performed on the head_to_head foreign key plus the action_number
    # to figure out what is being changed
    # 
    #
    # also, this means I need to create all of the individual games first, because they need to all be 
    # modifiable from the table interface, so I guess THAT'S the next step - implement the funcionality to 
    # create all games and everything else related to the head_to_head
    pass


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

        all_bowlers = get_all_bowlers()
        output_to_multiple_columns(all_bowlers)

        # TODO: I don't know when this stuff will be implemented, but this is a reminder to make it so 
        # player positions can be swapped after they're input, which is probably going to be a complicated process
        print("\nabove is a list of all bowlers (hopefully with some team info eventually)")
        print("using those ids, enter the ids of all 10 (make this dynamic?) bowlers, separated by spaces")
        print("starting with the first bowler on the left lane, then the second, etc., going down the list")
        print("of bowlers on the left lane and then bowlers on the right lane")
        print("optionally, add a comma and a value for handicap after each bowler id, separated by spaces")
        print("for example, this is an input of 8 bowler ids:")
        print("1 2 3 4 5 6 7 8")
        print("and this is an input for 6 bowlers with their handicaps:")
        print("1,10 2,50 3,22 4,30 5,0 6,11")

        bowler_list = get_bowler_ids()
        if not bowler_list:
            continue
        print(f"just making sure: {bowler_list}")

        new_head_to_head = create_head_to_head(new_week, teams[0].id, teams[1].id, the_season.id)
        # need to create bowler_head_to_head_game, head_to_head_game, no_handicap
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

    def write_data_to_table(left_dict, right_dict):
        # left_dict = {"name": "Name", "handicap": "HDCP", "games": [[200, 250], [100, 150], [50, 100]], "total": [599, 666], "points": "Pts"}
        left_string = "|"
        right_string = "|"

        left_string += f" {left_dict['name']: <{characters_per_name}} |"
        right_string += f" {right_dict['name']: <{characters_per_name}} |"

        left_string += f" {left_dict['handicap']: <{characters_per_handicap}} |"
        right_string += f" {right_dict['handicap']: <{characters_per_handicap}} |"

        for each_game in left_dict["games"]:
            left_string += f" {each_game[0]: <{characters_per_scratch_game}} {each_game[1] :<{characters_per_handicap_game}} |"

        for each_game in right_dict["games"]:
            right_string += f" {each_game[0]: <{characters_per_scratch_game}} {each_game[1] :<{characters_per_handicap_game}} |"

        left_string += f" {left_dict['total'][0]: <{characters_per_scratch_total}} {left_dict['total'][1]: <{characters_per_handicap_total}} |"
        right_string += f" {right_dict['total'][0]: <{characters_per_scratch_total}} {right_dict['total'][1]: <{characters_per_handicap_total}} |"

        left_string += f" {left_dict['points']: <{characters_per_points}} |"
        right_string += f" {right_dict['points']: <{characters_per_points}} |"

        print(f"{left_string}{right_string}")

    '''
    ansi escape codes for colors:
    grey: \033[90m'
    red: \033[91m'
    green: \033[92m'
    yellow: \033[93m'
    blue: \033[94m'
    purple: \033[95m'
    cyan: \033[96m'
    '''
    screen_width = 178

    characters_per_name = 25
    characters_per_handicap = 4
    characters_per_scratch_game = 4
    characters_per_handicap_game = 4
    characters_per_scratch_total = 5
    characters_per_handicap_total = 4
    characters_per_points = 3

    cell_padding = 2
    game_padding = 3

    # this is dummy data
    left_lane_num = 31
    num_games = 3
    left_team = "big ern"
    right_team = "pin tillers"
    left_bowlers = [["christian schoeller", 30], ["tony hertzkowitz", 55], ["duke dancombe", 10], ["dana dancombe", 5], ["mike vacha", 50]]
    right_bowlers = [["jeff sis", 2], ["mike mingo", 3], ["rick aguliar", 10], ["bill vitt", 10], ["brian manchura", 0]]

    name_width = ((characters_per_name + cell_padding) * 2) + 2
    hdcp_width = ((characters_per_handicap + cell_padding) * 2) + 2
    games_width = (((characters_per_scratch_game + characters_per_handicap_game + game_padding) * num_games) + (num_games)) * 2
    totals_width = ((characters_per_scratch_total + characters_per_handicap_total + game_padding + 1) * 2)
    points_width = (characters_per_points + cell_padding + 1) * 2

    total_width = name_width + hdcp_width + games_width + totals_width + points_width
    lane_padding = (total_width // 2) - 8
    team_padding = (total_width // 2) - 3

    divider_line = f"|{'-' * total_width}|"
    print(divider_line)
    print(f"| Lane {left_lane_num: <{lane_padding}} || Lane {left_lane_num + 1: <{lane_padding}} |")
    print(divider_line)
    print(f"| {left_team: <{team_padding}} || {right_team: <{team_padding}} |")
    print(divider_line)

    left_dict = {"name": "Name", "handicap": "hdcp", "games": [["1st", "hdcp"], ["2nd", "hdcp"], ["3rd", "hdcp"]], "total": ["Total", "hdcp"], "points": "Pts"}
    right_dict = {"name": "Name", "handicap": "hdcp", "games": [["1st", "hdcp"], ["2nd", "hdcp"], ["3rd", "hdcp"]], "total": ["Total", "hdcp"], "points": "Pts"}

    write_data_to_table(left_dict, right_dict)

    score_to_display = 110
    base_handicap = 10
    for name_position, name in enumerate(left_bowlers):

        print(divider_line)

        total_scratch = score_to_display * 3
        total_handicap = total_scratch + (base_handicap * 3)
        left_dict = {"name": name[0], "handicap": name[1], "games": [[score_to_display, base_handicap], [score_to_display, base_handicap], [score_to_display, base_handicap]], "total": [total_scratch, total_handicap], "points": 4}
        score_to_display += 10
        base_handicap += 5
        total_scratch = score_to_display * 3
        total_handicap = total_scratch + (base_handicap * 3)
        right_dict = {"name": right_bowlers[name_position][0], "handicap": right_bowlers[name_position][1], "games": [[score_to_display, base_handicap], [score_to_display, base_handicap], [score_to_display, base_handicap]], "total": [total_scratch, total_handicap], "points": 4}

        write_data_to_table(left_dict, right_dict)

    print(divider_line)

    left_dict = {"name": "Team Totals", "handicap": "250", "games": [[1000, 1500], [1000, 1500], [900, 950]], "total": [3500, 4500], "points": ""}
    right_dict = {"name": "Team Totals", "handicap": "250", "games": [[1000, 1500], [1000, 1500], [900, 950]], "total": [3500, 4500], "points": ""}

    left_string = "|"
    right_string = "|"

    # Names
    left_string += f" {'Team Totals': <{characters_per_name}} |"
    right_string += f" {'Team Totals': <{characters_per_name}} |"

    # handicaps
    left_string += f" {190: <{characters_per_handicap}} |"
    right_string += f" {109: <{characters_per_handicap}} |"

    # games
    for each_game in range(num_games):
        left_string += f" {'1010': <{characters_per_scratch_game}} {'999': <{characters_per_handicap_game}} |"
        right_string += f" {'998': <{characters_per_scratch_game}} {'1400': <{characters_per_handicap_game}} |"

    # totals
    left_string += f" {'3500': <{characters_per_scratch_total}} {'4800': <{characters_per_handicap_total}} |"
    right_string += f" {'3600': <{characters_per_scratch_total}} {'4200': <{characters_per_handicap_total}} |"

    # points
    left_string += f" {'':<{characters_per_points}} |"
    right_string += f" {'':<{characters_per_points}} |"

    print(f"{left_string}{right_string}")
    print(divider_line)
    print(divider_line)



