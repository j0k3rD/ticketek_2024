from fastapi import APIRouter, Depends, Path
from models import Events
from sqlmodel import Session
from src.config.db import get_session
from typing import Annotated
from src.services.event_service import (
    get_events,
    get_event,
    update_event,
    delete_event,
    create_event,
)

event = APIRouter()


@event.get("/events", tags=["events"])
def get_events_route(session: Session = Depends(get_session)) -> list[Events]:
    return get_events(session)


@event.get(
    "/events/{event_id}",
    response_model=Events,
    tags=["events"],
)
def get_event_route(
    event_id: Annotated[int, Path(name="The event ID")],
    session: Session = Depends(get_session),
) -> Events:
    return get_event(session, event_id)


@event.patch("/events/{event_id}", tags=["events"])
def update_event_route(
    event_id: int,
    event_data: Events,
    session: Session = Depends(get_session),
) -> Events:
    return update_event(session, event_id, event_data)


@event.delete("/events/{event_id}", tags=["events"])
def delete_event_route(
    event_id: int,
    session: Session = Depends(get_session),
) -> Events:
    delete_event(session, event_id)


@event.post("/events", tags=["events"])
def create_event_route(
    event_data: Events, session: Session = Depends(get_session)
) -> Events:
    return create_event(session, event_data)
