from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db import engine
from app.routes import heroes, team


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    create_db_and_tables()

    yield

    # Run on shutdown


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


app.include_router(heroes.router)
app.include_router(team.router)
