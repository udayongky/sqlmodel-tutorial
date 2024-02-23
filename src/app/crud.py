from sqlmodel import Session, or_, select

from .db import engine
from .models import Hero


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        # save all the data to the database
        session.commit()

        # fetch fresh data from the database
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90))
        heroes = session.exec(statement).all()
        print(heroes)
