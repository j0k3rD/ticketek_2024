from fastapi import APIRouter, Depends, Path, HTTPException
from src.database.db import get_session
from src.database.models import Event, Registration
from typing import Annotated
from sqlmodel import Session, select
# from src.routes.auth import RoleChecker
from src.services.registration_service import (
    get_registrations_by_dni,
    create_registration,
)
# from src.admin.admin_services import (
#     update_event,
#     delete_event
# )

registration = APIRouter()


@registration.get("/events/registrations/{dni}", tags=["registrations"])
def get_registrations_by_dni_route(
    dni: Annotated[int, Path(name="The DNI")],
    session: Session = Depends(get_session),
) -> Registration:
    return get_registrations_by_dni(session, dni)


@registration.post("/events/{event_id}/registrations", tags=["registrations"])
def create_registration_route(
    event_id: Annotated[int, Path(name="The Event ID")],
    registration_data: Registration,
    session: Session = Depends(get_session),
) -> Registration:
    return create_registration(session, registration_data)


#! SOLO PARA ADMIN
# @registration.get("/registrations", tags=["registrations"])
# def get_registrations_route(session: Session = Depends(get_session)) -> list[Registration]:
#     return get_registrations(session)

# @registration.put("/events/registrations/{registration_id}/approve", tags=["registrations"])
# def approve_registration_route(
#     registration_id: Annotated[int, Path(name="The Registration ID")],
#     session: Session = Depends(get_session),
# ) -> Registration:
#     return approve_registration(session, registration_id)