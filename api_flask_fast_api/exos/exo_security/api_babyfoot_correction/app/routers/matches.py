"""
Routes de gestion des matchs.
Matchs autorisés :
- single : joueur contre joueur
- team   : équipe contre équipe
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.match import Match
from app.models.player import Player
from app.models.schemas import MatchCreate, MatchResponse
from app.models.team import Team
from app.models.user import User

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    payload: MatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.participant_1_id == payload.participant_2_id:
        raise HTTPException(status_code=400, detail="Un participant ne peut pas jouer contre lui-même")

    if payload.match_type == "single":
        participant_1 = db.get(Player, payload.participant_1_id)
        participant_2 = db.get(Player, payload.participant_2_id)
        if participant_1 is None or participant_2 is None:
            raise HTTPException(status_code=400, detail="Les deux joueurs doivent exister")

    elif payload.match_type == "team":
        participant_1 = db.get(Team, payload.participant_1_id)
        participant_2 = db.get(Team, payload.participant_2_id)
        if participant_1 is None or participant_2 is None:
            raise HTTPException(status_code=400, detail="Les deux équipes doivent exister")

    match = Match(
        match_type=payload.match_type,
        participant_1_id=payload.participant_1_id,
        participant_2_id=payload.participant_2_id,
        score_1=payload.score_1,
        score_2=payload.score_2,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.get("", response_model=list[MatchResponse])
def list_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.execute(select(Match).order_by(Match.id)).scalars().all()


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    match = db.get(Match, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match introuvable")
    return match
