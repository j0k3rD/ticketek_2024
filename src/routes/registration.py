from fastapi import APIRouter, Depends, Path, HTTPException
from src.database.db import get_session
from src.database.models import Event, Registration
from typing import Annotated
from sqlmodel import Session, select
# from src.routes.auth import RoleChecker
from src.services.registration_service import (
    get_registrations_by_dni,
    # delete_registration,
    create_registration
)

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
