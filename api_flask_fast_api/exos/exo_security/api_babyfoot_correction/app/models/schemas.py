"""
Schémas Pydantic utilisés pour :
- valider les données entrantes
- structurer les réponses JSON sortantes
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    full_name: Optional[str] = Field(default=None, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PlayerCreate(BaseModel):
    nickname: str = Field(min_length=1, max_length=80)


class PlayerResponse(BaseModel):
    id: int
    nickname: str

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    player_1_id: int
    player_2_id: int


class TeamResponse(BaseModel):
    id: int
    name: str
    player_1: PlayerResponse
    player_2: PlayerResponse

    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    match_type: Literal["single", "team"]
    participant_1_id: int
    participant_2_id: int
    score_1: int = Field(ge=0)
    score_2: int = Field(ge=0)


class MatchResponse(BaseModel):
    id: int
    match_type: str
    participant_1_id: int
    participant_2_id: int
    score_1: int
    score_2: int

    class Config:
        from_attributes = True


class RankingItem(BaseModel):
    id: int
    name: str
    played: int
    wins: int
    losses: int
    draws: int
    goals_for: int
    goals_against: int
    goal_difference: int
