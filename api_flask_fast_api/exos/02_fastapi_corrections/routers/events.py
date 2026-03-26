from fastapi import APIRouter, HTTPException, status
import db.memory as memory
from models.event import Event

router = APIRouter(tags=["Events"])


@router.post("/events", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_event(event: Event):
    event_dict = event.model_dump()
    event_dict["id"] = memory.next_event_id
    memory.events_db[memory.next_event_id] = event_dict
    memory.next_event_id += 1
    return event_dict


@router.get("/events/{event_id}", response_model=dict)
async def get_event(event_id: int):
    if event_id not in memory.events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found"
        )
    return memory.events_db[event_id]