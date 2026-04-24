from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///.////sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    DataBase = SessionLocal()
    try:
        yield DataBase
    finally:
        DataBase.close()