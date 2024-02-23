from sqlmodel import SQLModel

from .db import engine
from .crud import create_heroes, select_heroes


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
