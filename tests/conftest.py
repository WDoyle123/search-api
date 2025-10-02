import os
import sys

os.environ.setdefault("DATABASE_HOSTNAME", "localhost")
os.environ.setdefault("DATABASE_PORT", "5432")
os.environ.setdefault("DATABASE_PASSWORD", "password")
os.environ.setdefault("DATABASE_NAME", "test_db")
os.environ.setdefault("DATABASE_USERNAME", "user")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from app import models 
from app.config import settings
from app.db import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

import app.db
app.db.engine = engine
app.db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TestingSessionLocal = app.db.SessionLocal

from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def seed_hotels(db_session):
    hotels = [
        models.Hotels(hotelID=101, latitude=51.5033, longitude=-0.1195),
        models.Hotels(hotelID=102, latitude=51.5094, longitude=-0.1183),
        models.Hotels(hotelID=103, latitude=51.4952, longitude=-0.1469),
    ]

    db_session.add_all(hotels)
    db_session.commit()

    return [
        {
            "hotelID": hotel.hotelID,
            "latitude": hotel.latitude,
            "longitude": hotel.longitude,
        }
        for hotel in hotels
    ]


@pytest.fixture
def seed_events(db_session):
    events = [
        models.Events(eventID=1, latitude=51.5007, longitude=-0.1246),
    ]

    db_session.add_all(events)
    db_session.commit()

    return [
        {
            "eventID": event.eventID,
            "latitude": event.latitude,
            "longitude": event.longitude,
        }
        for event in events
    ]

