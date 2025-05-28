from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

Base = declarative_base()
SessionLocal = None


def init_db(in_memory=False) -> Session:
    global SessionLocal

    if in_memory:
        db_url = "sqlite:///:memory:"
    else:
        db_url = "sqlite:///casino.db"

    engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    return SessionLocal()
