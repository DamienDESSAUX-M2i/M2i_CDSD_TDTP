"""
Routes de gestion des équipes.
Une équipe doit contenir exactement 2 joueurs différents.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.player import Player
from app.models.schemas import TeamCreate, TeamResponse
from app.models.team import Team
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.player_1_id == payload.player_2_id:
        raise HTTPException(status_code=400, detail="Une équipe doit contenir deux joueurs différents")

    existing_team = db.execute(
        select(Team).where(Team.name == payload.name)
    ).scalar_one_or_none()
    if existing_team:
        raise HTTPException(status_code=400, detail="Ce nom d'équipe existe déjà")

    player_1 = db.get(Player, payload.player_1_id)
    player_2 = db.get(Player, payload.player_2_id)

    if player_1 is None or player_2 is None:
        raise HTTPException(status_code=400, detail="Les deux joueurs doivent exister")

    team = Team(
        name=payload.name,
        player_1_id=payload.player_1_id,
        player_2_id=payload.player_2_id,
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    team = db.execute(
        select(Team)
        .options(joinedload(Team.player_1), joinedload(Team.player_2))
        .where(Team.id == team.id)
    ).scalar_one()

    return team


@router.get("", response_model=list[TeamResponse])
def list_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.execute(
        select(Team).options(joinedload(Team.player_1), joinedload(Team.player_2)).order_by(Team.id)
    ).scalars().all()


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    team = db.execute(
        select(Team).options(joinedload(Team.player_1), joinedload(Team.player_2)).where(Team.id == team_id)
    ).scalar_one_or_none()

    if team is None:
        raise HTTPException(status_code=404, detail="Équipe introuvable")
    return team
