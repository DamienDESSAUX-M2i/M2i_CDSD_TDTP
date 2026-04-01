"""
Endpoints bonus de classement.
Le classement est volontairement simple :
- matchs joués
- victoires
- défaites
- nuls
- buts pour / contre
- différence de buts
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.match import Match
from app.models.player import Player
from app.models.schemas import RankingItem
from app.models.team import Team
from app.models.user import User

router = APIRouter(prefix="/rankings", tags=["Rankings"])


def _empty_stats(entity_id: int, name: str) -> dict:
    return {
        "id": entity_id,
        "name": name,
        "played": 0,
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_difference": 0,
    }


@router.get("/players", response_model=list[RankingItem])
def players_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    players = db.execute(select(Player).order_by(Player.id)).scalars().all()
    matches = db.execute(select(Match).where(Match.match_type == "single")).scalars().all()

    stats = {player.id: _empty_stats(player.id, player.nickname) for player in players}

    for match in matches:
        p1 = stats.get(match.participant_1_id)
        p2 = stats.get(match.participant_2_id)
        if p1 is None or p2 is None:
            continue

        p1["played"] += 1
        p2["played"] += 1

        p1["goals_for"] += match.score_1
        p1["goals_against"] += match.score_2

        p2["goals_for"] += match.score_2
        p2["goals_against"] += match.score_1

        if match.score_1 > match.score_2:
            p1["wins"] += 1
            p2["losses"] += 1
        elif match.score_1 < match.score_2:
            p2["wins"] += 1
            p1["losses"] += 1
        else:
            p1["draws"] += 1
            p2["draws"] += 1

    for item in stats.values():
        item["goal_difference"] = item["goals_for"] - item["goals_against"]

    return sorted(
        stats.values(),
        key=lambda item: (item["wins"], item["goal_difference"], item["goals_for"]),
        reverse=True,
    )


@router.get("/teams", response_model=list[RankingItem])
def teams_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    teams = db.execute(select(Team).order_by(Team.id)).scalars().all()
    matches = db.execute(select(Match).where(Match.match_type == "team")).scalars().all()

    stats = {team.id: _empty_stats(team.id, team.name) for team in teams}

    for match in matches:
        t1 = stats.get(match.participant_1_id)
        t2 = stats.get(match.participant_2_id)
        if t1 is None or t2 is None:
            continue

        t1["played"] += 1
        t2["played"] += 1

        t1["goals_for"] += match.score_1
        t1["goals_against"] += match.score_2

        t2["goals_for"] += match.score_2
        t2["goals_against"] += match.score_1

        if match.score_1 > match.score_2:
            t1["wins"] += 1
            t2["losses"] += 1
        elif match.score_1 < match.score_2:
            t2["wins"] += 1
            t1["losses"] += 1
        else:
            t1["draws"] += 1
            t2["draws"] += 1

    for item in stats.values():
        item["goal_difference"] = item["goals_for"] - item["goals_against"]

    return sorted(
        stats.values(),
        key=lambda item: (item["wins"], item["goal_difference"], item["goals_for"]),
        reverse=True,
    )
