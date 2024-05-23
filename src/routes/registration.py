from fastapi import APIRouter, Depends, Path, Body
from src.database.db import get_session
from src.database.models import Registration
from typing import Annotated
from sqlmodel import Session

from src.services.registration_service import (
    get_registrations_by_dni,
    create_registration,
    delete_registration,
)

from src.admin.admin_services import (
    update_event,
    delete_event,
    approve_registration,
    get_registrations,
)

registration = APIRouter()


@registration.get("/registrations/{dni}", tags=["registrations"])
def get_registrations_by_dni_route(
    dni: Annotated[int, Path(name="The DNI")],
    session: Session = Depends(get_session),
) -> list[Registration]:
    return get_registrations_by_dni(session, dni)


@registration.delete("/registrations/{token}", tags=["registrations"])
def delete_registration_route(
    token: Annotated[str, Path(name="The Registration Token")],
    session: Session = Depends(get_session),
) -> Registration:
    # Return message
    return delete_registration(session, token)


#! SOLO PARA ADMIN
# @registration.get("/registrations", tags=["registrations"])
# def get_registrations_route(
#     session: Session = Depends(get_session),
# ) -> list[Registration]:
#     return get_registrations(session)


# @registration.put(
#     "/events/registrations/{registration_id}/approve", tags=["registrations"]
# )
# def approve_registration_route(
#     registration_id: Annotated[int, Path(name="The Registration ID")],
#     session: Session = Depends(get_session),
# ) -> Registration:
#     return approve_registration(session, registration_id)
