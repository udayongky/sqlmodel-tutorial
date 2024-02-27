from sqlmodel import SQLModel

from .crud import create_heroes, delete_heroes, select_heroes, update_heroes
from .db import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    update_heroes()
    delete_heroes()


if __name__ == "__main__":
    main()
