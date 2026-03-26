from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventType(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class Event(BaseModel):
    type: EventType = Field(..., description="Type d'événement: online ou offline")
    title: str = Field(..., min_length=1, description="Titre de l'événement")
    location: Optional[str] = Field(None, description="Lieu (requis si type=offline)")
    url: Optional[str] = Field(None, description="URL (requis si type=online)")
    max_participants: int = Field(1, ge=1, description="Nombre max de participants")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "online",
                    "title": "Web Seminar",
                    "url": "https://zoom.us/meeting",
                    "max_participants": 500
                },
                {
                    "type": "offline",
                    "title": "Workshop",
                    "location": "Paris, France",
                    "max_participants": 50
                }
            ]
        }
    )

    @model_validator(mode="after")
    def check_event_fields(self):
        if self.type == EventType.OFFLINE and not self.location:
            raise ValueError("location is required for offline events")

        if self.type == EventType.ONLINE and not self.url:
            raise ValueError("url is required for online events")

        return self