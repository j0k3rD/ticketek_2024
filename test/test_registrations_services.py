from conftest import TestingSessionLocal, test_event, registration_data, registration_data_2
from src.database.models import Event, Registration
from datetime import datetime
from src.services.registration_service import create_registration, get_registrations_by_dni, get_registrations_by_dni, delete_registration, token_in_registrations
from fastapi import HTTPException
import pytest


def test_create_registration():
    with TestingSessionLocal() as session:
        event = Event(
            title="Test Event",
            description="This is a test event.",
            address="123 Test St",
            max_attendees=100,
            date=datetime.strptime("2024-12-31", "%Y-%m-%d"),
            location="Test Location",
        )
        session.add(event)
        session.commit()

    registration_data = Registration(
        name="John Doe",
        email="john.doe@test.com",
        phone=2612345678,
        dni=98765432,
        status="pending",
    )

    registration = create_registration(session, 1, registration_data)

    assert registration.name == "John Doe"
    assert registration.email == "john.doe@test.com"
    assert registration.phone == "2612345678"
    assert registration.dni == 98765432
    assert registration.status == "pending"
    assert registration.event_id == 1


def test_create_registration_fail_event_not_exist():
    with TestingSessionLocal() as session:
        registration_data = Registration(
            name="John Doe",
            email="test@test.com",
            phone=2612345678,
            dni=12345678,
            status="pending",
        )

    with pytest.raises(HTTPException) as excinfo:
        create_registration(session, 999, registration_data)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Event does not exist."


def test_create_registration_service_event_full(test_event: Event, registration_data: Registration, registration_data_2: Registration):
    event, session = test_event

    registration_data.event_id = event.id
    registration_data_2.event_id = event.id

    session.add(registration_data)
    session.add(registration_data_2)

    session.commit()
    session.refresh(registration_data)

    with pytest.raises(HTTPException) as excinfo:
        create_registration(session, event.id, registration_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Event is full."


def test_get_registrations_by_dni(test_event: Event, registration_data: Registration):
    event, session = test_event

    registration_data.event_id = event.id
    session.add(registration_data)
    session.commit()
    session.refresh(registration_data)

    registrations = get_registrations_by_dni(session, registration_data.dni)

    assert len(registrations) >= 1
    assert any(registration.name == registration_data.name for registration in registrations)


def test_get_registrations_by_dni_not_found():
    with TestingSessionLocal() as session:
        with pytest.raises(HTTPException) as excinfo:
            get_registrations_by_dni(session, 99999999)
        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Registration not found"


def test_delete_registration_service(test_event, registration_data):
    event, session = test_event

    registration_data.event_id = event.id
    session.add(registration_data)
    session.commit()
    session.refresh(registration_data)

    token = registration_data.token

    deleted_registration = delete_registration(session, token)

    with pytest.raises(HTTPException):
        token_in_registrations(session, token)

    assert deleted_registration.id == registration_data.id

    event = session.query(Event).filter(Event.id == event.id).first()
    assert str(deleted_registration.id) not in event.attendees