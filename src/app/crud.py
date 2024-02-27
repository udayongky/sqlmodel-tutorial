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
        # statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90))

        # Select with Offset to skip rows and Limit to limit the results
        statement = select(Hero).offset(3).limit(3)

        # iterate over results
        # results = session.exec(statement)
        # for hero in results:
        #     print(hero)

        # return a list
        heroes = session.exec(statement).all()
        print(heroes)

        # read first row
        # hero = session.exec(statement).first()
        # print(hero)

        # exactly one row matching
        # hero = session.exec(statement).one()
        # print(hero)

        # select by id
        hero = session.get(Hero, 1)
        print(hero)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        statement = select(Hero).where(Hero.name == "Captain North America")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)

        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)

        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

        print("Updated hero 1:", hero_1)
        print("Updated hero 2:", hero_2)


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        session.delete(hero)
        session.commit()

        print("Deleted hero:", hero)

        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Spider-Youngster")
