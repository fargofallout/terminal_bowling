from pathlib import Path
import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.model_base import SqlAlchemyBase


__db_session = None

def global_init(db_file):
    global __db_session

    if __db_session:
        return

    if not db_file or not db_file.strip():
        raise Exception("db file must be specified")

    folder = Path(db_file).parent
    # print(f"this is the folder I'm going to create: {folder}")
    folder.mkdir(parents=True, exist_ok=True)

    engine = sa.create_engine(f"sqlite:///{db_file.strip()}")
    __db_session = orm.sessionmaker(bind=engine)

    import data.bowler
    import data.team
    import data.alley
    import data.league
    import data.season

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __db_session

    if not __db_session:
        raise Exception("you must call global_init() before this can be used")

    session = __db_session()
    session.expire_on_commit = False

    return session


