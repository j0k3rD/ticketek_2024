from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_registration(mock_db_session):
    response = client.post(
        "/events/1/registrations/",
        json={
            "name": "Test Event",
            "email": "test@email.com",
            "phone": "123456789",
            "dni": "123456789",

        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["email"] == "test@email.com"
    assert data["phone"] == "123456789"
    assert data["dni"] == "123456789"

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


#test de fallo 

def test_create_registration_fail(mock_db_session):
    
    mock_db_session.get.return_value = None
    
    response = client.post(
        "/events/1/registrations/",
        json={
            "name": "Test Event",
            "email": "test@email.com",
            "phone": "123456789",
            "dni": "123456789",
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event does not exist"

    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()