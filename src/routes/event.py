from fastapi import APIRouter, Depends, Path
from src.database.models import Event
from sqlmodel import Session
from src.database.db import get_session
from typing import Annotated
from src.services.event_service import (
    get_events,
    get_event,
    get_event_by_name,
    create_event
)

event = APIRouter()

@event.get("/events", tags=["events"])
def get_events_route(session: Session = Depends(get_session)) -> list[Event]:
    return get_events(session)


@event.get(
    "/events/{id}",
    response_model=Event,
    tags=["events"],
)
def get_event_route(
    id: Annotated[int, Path(name="The Event ID")],
    session: Session = Depends(get_session),
) -> Event:
    return get_event(session, id)


@event.get(
    "/events/by-name/{name}",
    response_model=Event,
    tags=["events"],
)
def get_event_by_name_route(
    name: Annotated[str, Path(name="The Event Name")],
    session: Session = Depends(get_session),
) -> Event:
    return get_event_by_name(session, name)


@event.post("/events", response_model=Event, tags=["events"])
def create_event_route(
    event_data: Event,
    session: Session = Depends(get_session),
) -> Event:
    return create_event(session, event_data)