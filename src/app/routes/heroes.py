from fastapi import APIRouter, HTTPException, Query
from passlib.context import CryptContext
from sqlmodel import Session, select

from ..db import engine
from ..models import Hero, HeroCreate, HeroRead, HeroUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


router = APIRouter()


@router.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate):
    hashed_password = get_password_hash(hero.password)
    with Session(engine) as session:
        extra_data = {"hashed_password": hashed_password}
        db_hero = Hero.model_validate(hero, update=extra_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@router.get("/heroes/", response_model=list[HeroRead])
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes


@router.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero


@router.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
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
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
