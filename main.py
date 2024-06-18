import sqlalchemy as sa
import sqlalchemy.orm as orm
from rich import print
import os
import data.db_session as db_session
import services.bowler_service as bowler_service


def init_db():
    db_name = "bowling.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    db_session.global_init(db_name)



if __name__ == "__main__":
    init_db()
    first_name = "mike"
    last_name = "vacha"
    bowler_service.create_bowler(first_name, last_name)
    bowler_service.get_bowler(first_name)
    

    # print("in main")
    # print("enter 1 to begin a new night")
    # print("enter 2 to add new bowler")
    # print("enter 3 to add a new team")
    # print("enter 4 to add a new league")
    # print("enter 5 to add a new season")
    #
    # input_choice = input("\nyour input? ")
    # print(f"you chose {input_choice}")


