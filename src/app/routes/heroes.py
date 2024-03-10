from fastapi import APIRouter
from sqlmodel import Session, select

from ..db import engine
from ..models import Hero

router = APIRouter()


@router.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@router.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
