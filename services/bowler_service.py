import sqlalchemy as sa
from data.models import Bowler
import data.db_session as db_session


def create_bowler(first_name):
    new_bowler = Bowler(first_name=first_name)
    session = db_session.create_session()
    session.add(new_bowler)
    session.commit()
    session.close()


def get_bowler(first_name):
    session = db_session.create_session()

    something = session.execute(sa.select(Bowler).where(Bowler.first_name == first_name)).scalar_one()
    print(f"did that work? {something}")


