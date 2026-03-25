from enum import StrEnum
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field, model_validator


class EventType(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"


class Evenement(BaseModel):
    type: EventType = Field(
        ...,
        title="Type d'événement",
        description="Indique si l'événement est en ligne ou en présentiel",
        example="online",
    )
    title: str = Field(
        ...,
        title="Titre",
        description="Titre de l'événement",
        example="Titi et Grosminet",
    )
    location: Optional[str] = Field(
        None,
        title="Lieu",
        description="Lieu de l'événement (obligatoire si offline)",
        example="Lille",
    )
    url: Optional[str] = Field(
        None,
        title="URL",
        description="Lien de l'événement (obligatoire si online)",
        example="https://example.com",
    )
    max_participants: int = Field(
        ...,
        ge=1,
        title="Nombre maximum de participants",
        description="Nombre maximum de participants autorisés (>= 1)",
        example=100,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "online",
                "title": "Titi et Grosminet",
                "location": "Lille",
                "url": "https://example.com",
                "max_participants": 100,
            }
        }
    }

    @model_validator(mode="after")
    def check_conditions(self):
        if self.type == EventType.OFFLINE:
            if not self.location:
                raise ValueError("location est obligatoire pour un événement offline")
        elif self.type == EventType.ONLINE:
            if not self.url:
                raise ValueError("url est obligatoire pour un événement online")
        return self


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/events/", response_model=Evenement, status_code=201)
def create_event(event: Evenement):
    return event
