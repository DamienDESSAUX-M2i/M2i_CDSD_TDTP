"""
Routes de gestion des joueurs.
Toutes les routes sont protégées par JWT.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.player import Player
from app.models.schemas import PlayerCreate, PlayerResponse
from app.models.user import User

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(
    payload: PlayerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_player = db.execute(
        select(Player).where(Player.nickname == payload.nickname)
    ).scalar_one_or_none()

    if existing_player:
        raise HTTPException(status_code=400, detail="Ce nickname existe déjà")

    player = Player(nickname=payload.nickname)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.get("", response_model=list[PlayerResponse])
def list_players(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.execute(select(Player).order_by(Player.id)).scalars().all()


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Joueur introuvable")
    return player
