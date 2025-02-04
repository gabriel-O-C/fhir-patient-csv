import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
