import sqlalchemy as sa
import sqlalchemy.orm as orm


__global_session = None

def global_init(db_file):
    global __global_session
    if __global_session:
        return

    conn_str = f"sqlite:///{db_file}"
    engine = sa.create_engine(conn_str, echo=False, connect_args={"check_same_thread": False})
    __global_session = orm.sessionmaker(bind=engine)
    import data.models as models
    # print(f"dir on this thing? {dir(models.Base)}")
    models.Base.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __global_session
    session: orm.Session = __global_session()
    session.expire_on_commit = False
    return session

