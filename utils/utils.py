import sqlalchemy as sa
import regex

from data import db_session
from data.bowler import Bowler
from data.team import Team
from data.alley import Alley
from data.league import League


def parse_global_options(user_input):
    match user_input:
        case "b" | "B":
            all_bowlers = get_all_bowlers()
            print("****************************")
            for each_bowler in all_bowlers:
                print(each_bowler)
            print("****************************")
            return True
        case "t" | "T":
            all_teams = get_all_teams()
            print("****************************")
            for each_team in all_teams:
                print(each_team)
            print("****************************")
            return True
        case "a" | "A":
            all_alleys = get_all_alleys()
            print("****************************")
            for each_alley in all_alleys:
                print(each_alley)
            print("****************************")
            return True
        case "l" | "L":
            all_leagues = get_all_leagues()
            print("****************************")
            for each_league in all_leagues:
                print(each_league)
            print("****************************")
            return True
        case _:
            return False


def get_all_bowlers():
    session = db_session.create_session()
    try:
        result = session.scalars(sa.select(Bowler).order_by(Bowler.id)).all()
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
        all_alleys = session.scalars(sa.select(Alley).order_by(Alley.id)).all()
        return all_alleys
    finally:
        session.close()


def get_all_leagues():
    session = db_session.create_session()
    try:
        all_leagues = session.scalars(sa.select(League).order_by(League.id)).all()
        return all_leagues
    finally:
        session.close()


def parse_formula(formula):
    print(f"this is the formula I need to parse: {formula}")
    # word_char_regex = regex.compile(r"\b(\B+)\b")

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
                token_list.append(current_token)
                current_token = ""
            if char != " ":
                if char in ["+", "-", "*", "/", "(", ")"]:
                    token_list.append(char)
                else:
                    print(f"{char} is not a valid token? please try again")
                    return False
    if len(current_token) > 0:
        token_list.append(current_token)
        current_token = ""

    print(token_list)

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
                print(f"at least two different variables were used: {variable_used} and {each_token}")
                print("I'm really trying to not make this too complicated, just use one variable for average")
                print("if two is actually necessary, I guess I'll deal with it")
                return False
            # print(f"during testing - this is the first var {variable_used}, and this is the current: {each_token}")

    # no variable in the formula
    if not variable_used:
        print("no variable in the league formula? that seems unlikely - try again (unless I know what I'm doing, in which case I have to rewrite)")
        return False

    print("still going")
    dummy_average = 170

