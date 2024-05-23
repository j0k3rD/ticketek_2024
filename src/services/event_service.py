from src.database.models import Event, Registration
from sqlmodel import Session, select
from fastapi import HTTPException


def get_events(session: Session) -> list[Event]:
    events = session.exec(select(Event)).all()
    for event in events:
        event.attendees = len(event.attendees)
    return events


def get_event(session: Session, event_id: int) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Events not found")
    return event


def get_event_by_name(session: Session, title: str) -> Event:
    event = session.exec(select(Event).where(Event.title == title)).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


def get_event_by_registration_id(session: Session, registration_id: int) -> Event:
    registrations = session.exec(
        select(Registration).where(Registration.id == registration_id)
    ).first()

    if registrations is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    event = session.get(Event, registrations.event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
