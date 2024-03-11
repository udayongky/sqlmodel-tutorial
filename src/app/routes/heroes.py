from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.deps import SessionDep
from app.models import Hero, HeroCreate, HeroRead, HeroReadWithTeam, HeroUpdate, Message
from app.security import get_password_hash

router = APIRouter()


@router.post("/heroes/", response_model=HeroRead)
def create_hero(session: SessionDep, hero: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(
        hero, update={"hashed_password": get_password_hash(hero.password)}
    )
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/heroes/", response_model=list[HeroRead])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Hero | None:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(session: SessionDep, hero_id: int) -> Any:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(session: SessionDep, hero_id: int, hero: HeroUpdate) -> Any:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        password = hero_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_hero.sqlmodel_update(hero_data, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete("/heroes/{hero_id}")
def delete_hero(session: SessionDep, hero_id: int) -> Message:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return Message(message="Hero deleted successfully")
