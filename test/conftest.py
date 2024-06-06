from unittest.mock import MagicMock, PropertyMock
import pytest
import sys,os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from src.database.db import get_session


mock_session = MagicMock()
type(mock_session).max_attendees = PropertyMock(return_value=100)
type(mock_session).registrations = PropertyMock(return_value=[MagicMock() for _ in range(10)])

mock_session.get.return_value = mock_session 


def override_get_session():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def mock_db_session():
    return mock_session