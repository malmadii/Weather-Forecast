import os
import tempfile
import pytest
from app import create_app


@pytest.fixture
def client(monkeypatch):
    """
    Creates a fresh Flask test client with a temporary DATA_PATH
    for every test. Ensures no real persistence file is ever touched.
    """
    # Create temp file to act as data.json
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    # Override DATA_PATH for this test session
    monkeypatch.setenv("DATA_PATH", temp_path)

    # Create app + client
    app = create_app()
    client = app.test_client()

    yield client

    # Cleanup
    os.remove(temp_path)


# --------------------------------------------------------
# TEST: POST should update the last city
# --------------------------------------------------------
def test_post_last_city_updates_value(client):
    """POST /api/last-city should store the provided city."""
    
    # Act
    response = client.post("/api/last-city", json={"last_city": "Tokyo"})
    
    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["last_city"] == "Tokyo"
    assert data["ok"] is True


# --------------------------------------------------------
# TEST: GET should return stored last city
# --------------------------------------------------------
def test_get_last_city_returns_stored_value(client):
    """GET /api/last-city should return the last stored city."""

    # First store a city
    client.post("/api/last-city", json={"last_city": "Berlin"})

    # Now retrieve it
    response = client.get("/api/last-city")

    assert response.status_code == 200
    data = response.get_json()
    assert data["last_city"] == "Berlin"


# --------------------------------------------------------
# TEST: POST should reject missing payload
# --------------------------------------------------------
def test_post_last_city_requires_value(client):
    """POST with no city should return 400 and an error message."""
    
    response = client.post("/api/last-city", json={})

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


# --------------------------------------------------------
# TEST: POST should reject empty city string
# --------------------------------------------------------
def test_post_last_city_rejects_empty(client):
    """POST with an empty string should return 400."""
    
    response = client.post("/api/last-city", json={"last_city": ""})

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
