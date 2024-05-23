from dotenv import load_dotenv
from src.database.db import get_session
from src.database.models import Event, Registration
from sqlmodel import Session, select
from fastapi import HTTPException
from src.utils.send_email import send_email
import random
from datetime import datetime

load_dotenv()

# --Eventos


def create_event(session: Session, event_data: Event) -> Event:
    correct_date = datetime.strptime(event_data.date, "%d-%m-%Y").strftime("%Y-%m-%d")

    event = Event(
        title=event_data.title,
        description=event_data.description,
        max_attendees=event_data.max_attendees,
        date=correct_date,
        location=event_data.location,
    )
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


# --Registrations


def get_registrations(session: Session) -> list[Registration]:
    return session.exec(select(Registration)).all()


def get_registration(session: Session, registration_id: int) -> Registration:
    return session.get(Registration, registration_id)


def get_registrations_by_event_id(
    session: Session, event_id: int
) -> list[Registration]:
    return session.exec(
        select(Registration).where(Registration.event_id == event_id)
    ).all()


def approve_registration(session: Session, registration_id: int) -> Registration:
    registration = session.get(Registration, registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.status = "approved"

    # General codigo random de 6 digitos para el token
    registration.token = "".join(random.choices("0123456789ABC", k=6))
    # Agregar el usuario a la lista de asistentes del evento
    event = session.get(Event, registration.event_id)

    # Guardar datos del usuario como un diccionario en la lista de asistentes
    event.attendees[registration.id] = {
        "name": registration.name,
        "email": registration.email,
        "phone": registration.phone,
        "dni": registration.dni,
        "token": registration.token,
    }

    session.add(registration)
    session.commit()
    session.refresh(registration)

    send_email(
        registration.email,
        "Registro Aprobado!",
        f"Su registro al evento {event.title} ha sido aprobado, su clave de validacion es {registration.token}.",
    )

    return registration
