from fastapi import APIRouter
from sqlmodel import Session, select

from ..db import engine
from ..models import Hero, HeroCreate, HeroRead

router = APIRouter()


@router.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@router.get("/heroes/", response_model=list[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
