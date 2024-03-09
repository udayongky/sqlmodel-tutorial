from sqlmodel import Session, or_, select

from .db import engine
from .models import Hero, Team


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        result = session.exec(statement)
        hero_deadpond = result.one()

        statement = select(Team).where(Team.id == hero_deadpond.team_id)
        result = session.exec(statement)
        team = result.first()
        print("Deadpond's team:", team)


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        hero_spider_boy.team_id = team_z_force.id
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)


def remove_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()

        hero_spider_boy.team_id = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("No Z force:", hero_spider_boy)


def delete_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()

        session.delete(hero_spider_boy)
        session.commit()

        print("Deleted hero:", hero_spider_boy)

        # Check deleted
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Spider-Boy")
