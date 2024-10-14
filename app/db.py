from sqlmodel import Session, SQLModel, create_engine

import models
from config import BaseConfig

config = BaseConfig()

DB_URL = f"postgresql+psycopg://{config.DB_USER_NAME}:{config.DB_USER_PASS}@{config.DB_HOST_NAME}:{config.DB_HOST_PORT}/{config.DB_NAME}"

engine = create_engine(f"{DB_URL}?options=-csearch_path%3Denv_backend", echo=config.DB_ECHO)


def get_db():
    return engine


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def reset_databese():
    engine = get_db()
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
