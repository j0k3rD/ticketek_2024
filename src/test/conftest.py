from unittest.mock import MagicMock
import pytest

from main import app
from src.database.db import get_session

mock_session = MagicMock()

def override_get_session():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def mock_db_session():
    return mock_session