from fastapi.testclient import TestClient
from app.main import app
from app.api.users import db
import pytest


@pytest.fixture
def client():
    db.clear()
    return TestClient(app)
