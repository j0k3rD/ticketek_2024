from src.services.event_service import get_events, get_event, get_event_by_name, get_event_by_registration_id
import pytest
from fastapi import HTTPException


def test_get_events(setup_events):
    session, event1, event2 = setup_events

    events = get_events(session)

    assert isinstance(events, list)
    assert len(events) == 2

    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"


def test_get_event(setup_events):
    session, event1, event2 = setup_events

    event = get_event(session, event1.id)

    assert event.title == "Event 1"


def test_get_event_failure(setup_events):
    session, event1, event2 = setup_events

    with pytest.raises(HTTPException) as exc_info:
        get_event(session, 999)

    assert exc_info.value.status_code == 404
    assert "Event with id 999 not found" in exc_info.value.detail



def test_get_event_by_name_success(setup_events):
    session, event1, event2 = setup_events

    event = get_event_by_name(session, "Event 2")

    assert event.title == "Event 2"


def test_get_event_by_name_failure(setup_events):
    session, event1, event2 = setup_events

    with pytest.raises(HTTPException) as exc_info:
        get_event_by_name(session, "Nonexistent Event")

    assert exc_info.value.status_code == 404
    assert "Event with title 'Nonexistent Event' not found" in exc_info.value.detail


def test_get_event_by_registration_id(setup_events, registration_data):
    session, event1, event2 = setup_events

    # Crear una inscripción para el evento 1
    registration_data.event_id = event1.id
    session.add(registration_data)
    session.commit()

    # Obtener el evento asociado a la inscripción
    event = get_event_by_registration_id(session, registration_data.id)

    assert event.title == "Event 1"


def test_get_event_by_registration_id_failure(setup_events, registration_data):
    session, event1, event2 = setup_events

    # Intentar obtener un evento con un ID de registro que no existe
    with pytest.raises(HTTPException) as exc_info:
        get_event_by_registration_id(session, 999)

    assert exc_info.value.status_code == 404
    assert "Registration with id 999 not found" in exc_info.value.detail