from conftest import client

def test_get_events(test_event):
    event, _ = test_event

    response = client.get("/events")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == event.title
    assert data[0]["description"] == event.description
    assert data[0]["address"] == event.address
    assert data[0]["max_attendees"] == event.max_attendees
    assert data[0]["date"] == event.date.isoformat()
    assert data[0]["location"] == event.location


def test_get_event_by_id(test_event):
    event, _ = test_event

    response = client.get(f"/events/{event.id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == event.title
    assert data["description"] == event.description
    assert data["address"] == event.address
    assert data["max_attendees"] == event.max_attendees
    assert data["date"] == event.date.isoformat()
    assert data["location"] == event.location


def test_get_event_by_id_not_found():
    response = client.get("/events/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event with id 9999 not found"


def test_get_event_by_name(test_event):
    event, _ = test_event

    response = client.get(f"/events/by-name/{event.title}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == event.title
    assert data["description"] == event.description
    assert data["address"] == event.address
    assert data["max_attendees"] == event.max_attendees
    assert data["date"] == event.date.isoformat()
    assert data["location"] == event.location


def test_get_event_by_name_not_found():
    non_existent_event_name = "Nonexistent Event"
    response = client.get(f"/events/by-name/{non_existent_event_name}")
    assert response.status_code == 404





