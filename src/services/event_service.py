from src.database.models import Event, Registration
from sqlmodel import Session, select
from fastapi import HTTPException


def get_events(session: Session) -> list[Event]:
    # Para SQLite
    events = session.query(Event).filter(Event.id > 0).all()
    if events is None:
        raise HTTPException(status_code=404, detail="Events not found")
    
    for event in events:
        event.attendees = len(event.attendees)
    return events


def get_event(session: Session, event_id: int) -> Event:
    event = session.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    return event


def get_event_by_name(session: Session, title: str) -> Event:
    event = session.query(Event).filter(Event.title == title).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with title '{title}' not found")
    return event


def get_event_by_registration_id(session: Session, registration_id: int) -> Event:
    registration = session.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail=f"Registration with id {registration_id} not found")
    
    event = session.query(Event).filter(Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event associated with registration id {registration_id} not found")
    return event
