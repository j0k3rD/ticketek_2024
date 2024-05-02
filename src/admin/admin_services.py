from dotenv import load_dotenv
from src.database.db import get_session
from src.database.models import Event, Registration
from sqlmodel import Session, select
from fastapi import HTTPException

load_dotenv()

#--Eventos

def update_event(session: Session, event_id: int, event_data: Event) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.name = event_data.name
    event.event_type = event_data.event_type

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def delete_event(session: Session, event_id: int) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(event)
    session.commit()


def create_event(session: Session, event_data: Event) -> Event:
    event = Event(
        created_at=event_data.created_at,
        name=event_data.name,
        event_type=event_data.event_type,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

#--Registrations

def get_registrations(session: Session) -> list[Registration]:
    return session.exec(select(Registration)).all()

def get_registration(session: Session, registration_id: int) -> Registration:
    return session.get(Registration, registration_id)

def get_registrations_by_event_id(session: Session, event_id: int) -> list[Registration]:
    return session.exec(select(Registration).where(Registration.event_id == event_id)).all()

def approve_registration(session: Session, registration_id: int) -> Registration:
    registration = session.get(Registration, registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.status = "approved"
    session.add(registration)
    session.commit()
    session.refresh(registration)
    return registration