from models import Events
from sqlmodel import Session, select
from fastapi import HTTPException


def get_events(session: Session) -> list[Events]:
    return session.exec(select(Events)).all()


def get_event(session: Session, event_id: int) -> Events:
    event = session.get(Events, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Events not found")
    return event


def update_event(session: Session, event_id: int, event_data: Events) -> Events:
    event = session.get(Events, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Events not found")

    event.name = event_data.name
    event.event_type = event_data.event_type

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def delete_event(session: Session, event_id: int) -> Events:
    event = session.get(Events, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Events not found")

    session.delete(event)
    session.commit()


def create_event(session: Session, event_data: Events) -> Events:
    event = Events(
        created_at=event_data.created_at,
        name=event_data.name,
        event_type=event_data.event_type,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
