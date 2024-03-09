from sqlmodel import Session, select

from .db import engine
from .models import Hero, HeroTeamLink, Team


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
        )
        deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
        deadpond_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_deadpond, is_training=True
        )
        spider_boy_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_spider_boy, is_training=True
        )
        rusty_man_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_rusty_man
        )

        session.add(deadpond_team_z_link)
        session.add(deadpond_preventers_link)
        session.add(spider_boy_preventers_link)
        session.add(rusty_man_preventers_link)
        session.commit()

        for link in team_z_force.hero_links:
            print("Z-Force hero:", link.hero, "is training:", link.is_training)

        for link in team_preventers.hero_links:
            print("Preventers hero:", link.hero, "is training:", link.is_training)


def select_heroes():
    with Session(engine) as session:
        team_preventers = session.exec(
            select(Team).where(Team.name == "Preventers")
        ).one()

        for link in team_preventers.hero_links:
            print(
                "Select preventers hero:", link.hero, "is training:", link.is_training
            )


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        spider_boy_z_force_link = HeroTeamLink(
            team=team_z_force, hero=hero_spider_boy, is_training=True
        )
        team_z_force.hero_links.append(spider_boy_z_force_link)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.team_links)
        print("Z-Force heroes:", team_z_force.hero_links)

        for link in hero_spider_boy.team_links:
            if link.team.name == "Preventers":
                link.is_training = False

        session.add(hero_spider_boy)
        session.commit()

        for link in hero_spider_boy.team_links:
            print("Spider-Boy team:", link.team, "is training:", link.is_training)


def remove_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        print("Before Remove Z-Force heroes:", team_z_force.hero_links)

        for link in team_z_force.hero_links:
            if link.hero.name == "Spider-Boy":
                session.delete(link)

        session.commit()

        print("Remove Spider-Boy's Teams:", hero_spider_boy.team_links)
        print("After Remove Z-Force heroes:", team_z_force.hero_links)


def delete_heroes():
    with Session(engine) as session:
        hero_deadpond = session.exec(select(Hero).where(Hero.name == "Deadpond")).one()
        for link in hero_deadpond.team_links:
            session.delete(link)

        session.delete(hero_deadpond)
        session.commit()

        print("Deleted hero:", hero_deadpond)

        # Check deleted hero
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("There's no hero named Deadpond")
