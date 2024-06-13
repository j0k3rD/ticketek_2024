import sys,os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
import pytest
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.models import Event, Registration
from src.database.db import get_session
from main import app

load_dotenv()


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup() -> None:
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

    
@pytest.fixture
def registration_data():
    return Registration(
        name="John Doe",
        email="john.doe@alumno.com",
        phone="2612345678",
        dni=12345678,
        status="pending",
    )

@pytest.fixture
def registration_data_2():
    return Registration(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="2612345679",
        dni=12345679,
        status="pending",
    )

@pytest.fixture(scope="function")
def test_event():
    session = TestingSessionLocal()
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
    session.refresh(event)
    yield event, session
    session.close()
    
@pytest.fixture
def test_event():
    session = TestingSessionLocal()
    event = Event(
        title="Test Event",
        description="This is a test event.",
        address="123 Test St",
        max_attendees=1,
        date=datetime.strptime("2024-12-31", "%Y-%m-%d"),
        location="Test Location",
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    yield event, session
    session.close()

@pytest.fixture(scope="function")
def setup_events():
    session = TestingSessionLocal()

    event1 = Event(
        title="Event 1",
        description="Description 1",
        address="Address 1",
        max_attendees=100,
        date=datetime.strptime("2024-12-31", "%Y-%m-%d"),
        location="Location 1",
    )
    session.add(event1)

    event2 = Event(
        title="Event 2",
        description="Description 2",
        address="Address 2",
        max_attendees=200,
        date=datetime.strptime("2024-12-31", "%Y-%m-%d"),
        location="Location 2",
    )
    session.add(event2)

    session.commit()
    yield session, event1, event2
    session.close()