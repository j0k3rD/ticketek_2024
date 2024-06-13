from conftest import client
import random


def test_create_registration(test_event):
    event, _ = test_event
    response = client.post(
        f"/events/{event.id}/registrations",
        json={
            "name": "John Doe",
            "email": "pepe@gmail.com",
            "phone": "2612345678",
            "dni": 12345678,
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "pepe@gmail.com"
    assert data["phone"] == "2612345678"
    assert data["dni"] == 12345678
    assert data["event_id"] == event.id
    assert "token" in data
    assert data["status"] == "pending"


def test_create_registration_fail_event_not_exist():
    response = client.post(
        "/events/9999/registrations",
        json={
            "name": "John Doe",
            "email": "test@gmail.com",
            "phone": "2612345678",
            "dni": 12345678,
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event does not exist."


def test_get_registrations_by_dni(test_event, registration_data):
    event, session = test_event
    registration_data.event_id = event.id
    session.add(registration_data)
    session.commit()
    session.refresh(registration_data)

    response = client.get(f"/registrations/{registration_data.dni}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(registration["name"] == registration_data.name for registration in data)


def test_get_registrations_by_dni_not_found():
    response = client.get("/registrations/99999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Registration not found"


def test_delete_registration_controller(test_event, registration_data):
    event, session = test_event
    registration_data.event_id = event.id

    # TODO PASAR A UNA FUNCION
    registration_data.token = "".join(random.choices("0123456789ABC", k=6))

    session.add(registration_data)
    session.commit()
    session.refresh(registration_data)

    token = registration_data.token

    assert token is not None

    response = client.delete(f"/registrations/{token}")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == registration_data.name
    assert data["email"] == registration_data.email
    assert data["phone"] == registration_data.phone
    assert data["dni"] == registration_data.dni


def test_delete_registration_controller_not_found():
    response = client.delete("/registrations/invalid_token")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Registration not found"
