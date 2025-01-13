import sqlalchemy as sa
import regex

from data import db_session
from data.bowler import Bowler
from data.team import Team
from data.alley import Alley
from data.league import League
from data.season import Season
from data.game import Game


def parse_global_options(user_input):
    match user_input:
        case "b" | "B":
            all_bowlers = get_all_bowlers()
            print("\n****************************")
            print("all bowlers")
            print("****************************")
            for each_bowler in all_bowlers:
                print(each_bowler)
            print("****************************")
            return True
        case "t" | "T":
            all_teams = get_all_teams()
            print("\n****************************")
            print("all teams")
            print("****************************")
            for each_team in all_teams:
                print(each_team)
            print("****************************")
            return True
        case "a" | "A":
            all_alleys = get_all_alleys()
            print("\n****************************")
            print("all alleys")
            print("****************************")
            for each_alley in all_alleys:
                print(each_alley)
            print("****************************")
            return True
        case "l" | "L":
            all_leagues = get_all_leagues()
            print("\n****************************")
            print("all leagues")
            print("****************************")
            for each_league in all_leagues:
                print(each_league)
            print("****************************")
            return True
        case "s" | "S":
            all_seasons = get_all_seasons()
            print("\n****************************")
            print("all seasons")
            print("****************************")
            for each_season in all_seasons:
                print(each_season)
            print("****************************")
            return True
        case "g" | "G":
            all_games = get_all_games()
            print("\n****************************")
            print("all games")
            print("****************************")
            for each_game in all_games:
                print(each_game)
            print("****************************")
            return True
        case "h" | "H":
            print("this is where I'd print the help, if there were to be any")
        case _:
            return False


def get_all_bowlers():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Bowler).order_by(Bowler.id)).unique().all()
        return result
    finally:
        session.close()


def get_all_teams():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Team).order_by(Team.id)).all()
        return result
    finally:
        session.close()


def get_all_alleys():
    session = db_session.create_session()
    try:
        # all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).all()
        all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).unique().all()
        return all_alleys
    finally:
        session.close()


def get_all_leagues():
    session = db_session.create_session()
    try:
        all_leagues = session.scalars(sa.select(League).order_by(League.id)).unique().all()
        return all_leagues
    finally:
        session.close()


def get_all_seasons():
    session = db_session.create_session()
    try:
        all_seasons = session.scalars(sa.select(Season).order_by(Season.id)).unique().all()
        return all_seasons
    finally:
        session.close()


def get_all_games():
    session = db_session.create_session()
    try:
        all_games = session.scalars(sa.select(Game).order_by(Game.id)).unique().all()
        return all_games
    finally:
        session.close()

def parse_formula(formula):
    print(f"this is the formula I need to parse: {formula}")

    current_token = ""
    token_list = []
    for char in formula:
        if regex.search(r"\d", char):
            current_token += char
        elif regex.search(r"\.", char):
            current_token += char
        elif regex.search(r"[a-zA-Z]+", char):
            current_token += char
        else:
            if len(current_token) > 0:
                # need to make sure the token isn't something like a0.90, which will get past the regexes above
                if regex.search(r"\d", current_token) and regex.search(r"[a-zA-Z]", current_token):
                    print(f"{current_token} is not a valid part of the formula, please try again")
                    return False
                token_list.append(current_token)
                current_token = ""
            if char != " ":
                if char in ["+", "-", "*", "/", "(", ")"]:
                    token_list.append(char)
                else:
                    print(f"{char} is not a valid token? please try again")
                    return False

    if len(current_token) > 0:
        if regex.search(r"\d", current_token) and regex.search(r"[a-zA-Z]", current_token):
            print(f"{current_token} is not a valid part of the formula, please try again")
            return False
        token_list.append(current_token)
        current_token = ""

    # chop off leading and trailing parentheses
    if token_list[0] == "(" and token_list[-1] == ")":
        token_list = token_list[1:-1]

    # make sure formula has the same number of open and closed parenthesis
    paren_balance = 0
    for each_token in token_list:
        if each_token == "(":
            paren_balance += 1
        elif each_token == ")":
            paren_balance -= 1

    if paren_balance != 0:
        if paren_balance < 0:
            print("there are too many closed parenthesis, please re-enter the formula")
        elif paren_balance > 0:
            print("there are too many open parenthesis, please re-enter the formula")
        return False

    # make sure at most one unique variable is used
    variable_used = ""
    word_regex = regex.compile(r"([a-zA-Z]+)")
    for each_token in token_list:
        word_match = word_regex.search(each_token)
        if word_match and not variable_used:
            variable_used = each_token
        elif word_match and variable_used:
            if each_token != variable_used:
                print(f"at least two different variables were used: '{variable_used}' and '{each_token}', which isn't allowed")
                print("I'm really trying to not make this too complicated, just use one variable for average")
                print("if two is actually necessary, I guess I'll deal with it")
                return False
            # print(f"during testing - this is the first var {variable_used}, and this is the current: {each_token}")

    # no variable in the formula
    if not variable_used:
        print("no variable in the league formula? that seems unlikely - try again (unless I know what I'm doing, in which case I have to rewrite)")
        return False

    if len(token_list) < 3:
        print("the length of the formula is less than three tokens, which doesn't seem legit - try again, or rewrite this when, in some")
        print("weird alternate history, the handicap formula is something sqroot(average) or something")
        return False

    # TODO: figure out how to validate to make sure values always come in pairs
    # e.g., (2 * average) and not (2 * average + 10)
    # maybe not important since I'll be the one entering the formula, but it should still be done
    return token_list

    # dummy_average = 170
    # calculated_value = recursive_calc_function(token_list, dummy_average)
    # print(f"good lord, if that actually worked: {calculated_value}")


def recursive_calc_function(token_list, bowler_average):
    # print(f"at the top of function - list: {token_list}")

    open_position = 0
    closed_position = 0
    paren_balance = 0
    currently_in_parens = False
    list_to_calculate = []
    for token_position, each_token in enumerate(token_list):

        # print(f"current token: {each_token}, am I currently in parens? {currently_in_parens}")
        if each_token == "(" and not currently_in_parens:
            open_position = token_position
            paren_balance += 1
            currently_in_parens = True
        elif each_token == "(" and currently_in_parens:
            paren_balance += 1
        elif each_token == ")" and currently_in_parens:
            paren_balance -= 1

        if currently_in_parens and paren_balance == 0:
            closed_position = token_position
            sub_list = token_list[open_position + 1:closed_position]
            currently_in_parens = False
            # print(f"????? {sub_list}")
            each_token = recursive_calc_function(sub_list, bowler_average)
            # print(f"got back from recursive call - token: {each_token}, status of parens? {currently_in_parens}")

        if not currently_in_parens:
            # print(f"wtf - current token: {each_token}, type: {type(each_token)}")
            # print(f"is the problem the list to calculate and the token list? {list_to_calculate}, {token_list}")

            if type(each_token) == type(50):
                list_to_calculate.append(each_token)
            elif type(each_token) == type(5.5):
                list_to_calculate.append(each_token)
            elif regex.search(r"^\d+$", each_token):
                list_to_calculate.append(int(each_token))
            elif regex.search(r"^\d*\.\d+$", each_token):
                list_to_calculate.append(float(each_token))
            elif regex.search(r"^[a-zA-Z]+$", each_token):
                list_to_calculate.append(bowler_average)
            elif each_token in ["+", "-", "*", "/"]:
                list_to_calculate.append(each_token)
            else:
                print("I shouldn't ever see this, something went wrong")

        if len(list_to_calculate) == 3:
            return_value = 0
            if list_to_calculate[1] == "+":
                return_value = list_to_calculate[0] + list_to_calculate[2]
            elif list_to_calculate[1] == "-":
                return_value = list_to_calculate[0] - list_to_calculate[2]
            elif list_to_calculate[1] == "*":
                return_value = list_to_calculate[0] * list_to_calculate[2]
            elif list_to_calculate[1] == "/":
                return_value = list_to_calculate[0] / list_to_calculate[2]

            # print(f"about to return - list to calc: {list_to_calculate}, calculated value: {return_value}")
            return return_value

