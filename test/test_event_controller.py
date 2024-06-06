from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_event(mock_db_session):
    response = client.post(
        "/events",
        json={
            "name": "Test Event",
            "date": "2023-01-01",
            "location": "Test Location",
            "price": 100,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["date"] == "2023-01-01"
    assert data["location"] == "Test Location"
    assert data["price"] == 100

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()