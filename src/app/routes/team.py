from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.deps import SessionDep
from app.models import (
    Message,
    Team,
    TeamCreate,
    TeamRead,
    TeamReadWithHeroes,
    TeamUpdate,
)

router = APIRouter()


@router.post("/teams/", response_model=TeamRead)
def create_team(session: SessionDep, team: TeamCreate) -> Team:
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/teams/", response_model=list[TeamRead])
def read_teams(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Team | None:
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamReadWithHeroes)
def read_team(session: SessionDep, team_id: int) -> Any:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    session: SessionDep,
    team_id: int,
    team: TeamUpdate,
) -> Any:
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}")
def delete_team(session: SessionDep, team_id: int) -> Message:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return Message(message="Team deleted successfully")
