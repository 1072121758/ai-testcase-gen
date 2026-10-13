import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))


from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def token(client):

    response = client.post(
        "/login",
        json={
            "username": "wendi",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]

@pytest.fixture
def auth_headers(token):

    return {
        "Authorization": f"Bearer {token}"
    }

