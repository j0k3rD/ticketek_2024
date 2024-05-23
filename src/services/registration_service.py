from src.database.models import Registration, Event
from sqlmodel import Session, select
from fastapi import HTTPException


def get_registrations_by_dni(session: Session, dni: int) -> Registration:
    registration = session.exec(
        select(Registration).where(Registration.dni == dni)
    ).first()
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


# def update_registration(session: Session, registration_id: int, registration_data: Registration) -> Registration:
#     registration = session.get(Registration, registration_id)
#     registration.name = registration_data.name
#     registration.email = registration_data.email
#     registration.phone = registration_data.phone
#     registration.dni = registration_data.dni
#     registration.status = registration_data.status
#     session.add(registration)
#     session.commit()
#     session.refresh(registration)
#     return registration


def delete_registration(
    session: Session, event_id: int, registration_id: int, token: str
) -> Registration:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = session.get(Registration, registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    if registration.token != token:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Obtener la lista de asistentes actual del evento
    attendees_list = dict(event.attendees) if event.attendees else {}

    # Eliminar el registro de la lista de asistentes
    if str(registration_id) in attendees_list:
        del attendees_list[str(registration_id)]

    # Actualizar la lista de asistentes del evento
    event.attendees = attendees_list

    session.delete(registration)
    session.add(event)
    session.commit()

    return registration


def create_registration(
    session: Session, event_id: int, registration_data: Registration
) -> Registration:

    registration = Registration(
        name=registration_data.name,
        email=registration_data.email,
        phone=registration_data.phone,
        dni=registration_data.dni,
        event_id=event_id,
    )

    event_check = session.get(Event, event_id)
    if event_check is None:
        raise HTTPException(status_code=404, detail="Event does not exist.")
    else:
        # Checkear si queda un espacio disponible en el evento para registrarse
        if event_check.max_attendees <= len(event_check.registrations):
            raise HTTPException(status_code=400, detail="Event is full.")

    # Checkear si el dni o el email ya están registrados en el evento
    email_and_dni_in_event = session.exec(
        select(Registration).where(Registration.event_id == registration_data.event_id)
    ).all()

    for existing_registration in email_and_dni_in_event:
        if existing_registration.dni == registration_data.dni:
            raise HTTPException(
                status_code=400, detail="DNI already registered in this event."
            )
        if existing_registration.email == registration_data.email:
            raise HTTPException(
                status_code=400, detail="Email already registered in this event."
            )

    session.add(registration)
    session.commit()
    session.refresh(registration)
    return registration


def get_registrations(session: Session) -> list[Registration]:
    return session.exec(select(Registration)).all()
