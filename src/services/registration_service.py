from src.database.models import Registration, Event
from sqlmodel import Session, select
from fastapi import HTTPException
from src.services.event_service import get_event_by_registration_id


def get_registrations_by_dni(session: Session, dni: int) -> list[Registration]:
    registration = session.query(Registration).filter(Registration.dni == dni).all()

    if not registration:
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


def token_in_registrations(session: Session, token: str) -> Registration:
    registration = session.query(Registration).filter(Registration.token == token).first()
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


def delete_registration(session: Session, token: str) -> Registration:
    registration = token_in_registrations(session, token)

    if registration.token != token:
        raise HTTPException(status_code=403, detail="Invalid token")

    print("REGISTRATION: ", registration.id)
    event = get_event_by_registration_id(session, registration.id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # Obtener la lista de asistentes actual del evento
    attendees_list = dict(event.attendees) if event.attendees else {}

    # Eliminar el registro de la lista de asistentes
    if str(registration.id) in attendees_list:
        del attendees_list[str(registration.id)]

    # Actualizar la lista de asistentes del evento
    event.attendees = attendees_list

    session.delete(registration)
    session.add(event)
    session.commit()

    return registration


def create_registration(
    session: Session, event_id: int, registration_data: Registration
) -> Registration:

    event_check = session.query(Event).filter(Event.id == event_id).first()
    if event_check is None:
        raise HTTPException(status_code=404, detail="Event does not exist.")
    else:
        # Checkear si queda un espacio disponible en el evento para registrarse
        if event_check.max_attendees <= len(event_check.registrations):
            raise HTTPException(status_code=400, detail="Event is full.")

        registration = Registration(**registration_data.model_dump(), event_id=event_id)

        # Checkear si el dni o el email ya están registrados en el evento
        email_and_dni_in_event = session.query(Registration).filter(
            Registration.event_id == event_id
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
