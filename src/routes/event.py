from fastapi import APIRouter, Depends, Path, Body
from src.database.models import Event
from sqlmodel import Session
from src.database.db import get_session
from typing import Annotated
from src.services.event_service import get_events, get_event, get_event_by_name

from src.admin.admin_services import update_event, delete_event, create_event

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


#! SOLO PARA ADMIN
# @event.post(
#     "/events",
#     response_model=Event,
#     tags=["events"],
# )
# def create_event_route(
#     event_data: Annotated[
#         Event,
#         Body(
#             examples=[
#                 {
#                     "title": "Event Title",
#                     "description": "Event Description",
#                     "max_attendees": 1000,
#                     "location": {"address": "San Martin 123, San Rafael"},
#                     "date": "31-12-2023",
#                 }
#             ]
#         ),
#     ],
#     session: Session = Depends(get_session),
# ) -> Event:
#     return create_event(session, event_data)
