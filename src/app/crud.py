from sqlmodel import Session, select

from .db import engine
from .models import Hero


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        # save all the data to the database
        session.commit()

        # fetch fresh data from the database
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        heroes = session.exec(statement).all()
        print(heroes)
