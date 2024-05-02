from src.database.models import Event
from sqlmodel import Session, select
from fastapi import HTTPException


def get_events(session: Session) -> list[Event]:
    return session.exec(select(Event)).all()

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

def create_event(session: Session, event_data: Event) -> Event:
    event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        max_attendees=event_data.max_attendees,
        )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event