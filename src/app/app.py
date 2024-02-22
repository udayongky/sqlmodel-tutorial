from sqlmodel import SQLModel

from .database import engine
from .seeders import create_heroes


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
