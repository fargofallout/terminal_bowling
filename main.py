import sqlalchemy as sa
import sqlalchemy.orm as orm
from rich import print
import data.db_session as db_session
import services.bowler_service as bowler_service


def init_db():
    db_session.global_init()


# engine = sa.create_engine("sqlite+pysqlite:///:memory:")
# # engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
# models.Base.metadata.create_all(engine)
# session = orm.Session(engine)

# a_bowler = models.Bowler(first_name = "mike")
# another_bowler = models.Bowler(first_name = "mike")
# session.add(a_bowler)
# session.add(another_bowler)
#
# session.commit()

# something = session.execute(sa.select(models.Bowler).where(models.Bowler.first_name == "mike")).scalar_one()
# print(something)

# something_two = session.execute(sa.select(models.Bowler).where(models.Bowler.first_name == "mike")).scalar()
# print(something_two)
# print(f"??? {type(something_two)}")
#
# something_three = session.execute(sa.select(models.Bowler).where(models.Bowler.first_name == "mike")).scalars()
# print(something_three)
# print(f"type? {type(something_three)}")
# for each_whatever in something_three:
#     print(f"this is the item: {each_whatever} and this is the type: {type(each_whatever)}")
#
# session.close()
#


if __name__ == "__main__":
    init_db()
    print("done?")
    bowler_name = "mike"
    bowler_service.create_bowler(bowler_name)
    bowler_service.get_bowler(bowler_name)
    

    # print("in main")
    # print("enter 1 to begin a new night")
    # print("enter 2 to add new bowler")
    # print("enter 3 to add a new team")
    # print("enter 4 to add a new league")
    # print("enter 5 to add a new season")
    #
    # input_choice = input("\nyour input? ")
    # print(f"you chose {input_choice}")


