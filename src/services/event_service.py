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

def get_event_by_name(session: Session, name: str) -> Event:
    event = session.exec(select(Event).where(Event.name == name)).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event