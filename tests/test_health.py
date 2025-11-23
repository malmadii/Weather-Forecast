import pytest
from app import create_app

@pytest.fixture
def client():
    """
    Creates a fresh Flask test client for every test.
    This follows pytest fixture best practices from the course.
    """
    app = create_app()
    return app.test_client()

def test_health_endpoint(client):
    """
    Ensure the /health endpoint returns a proper status payload.
    Checks:
    - 200 OK
    - JSON response
    - "status" key = "ok"
    - "uptime" present and numeric
    """

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, dict)
    assert data["status"] == "ok"
    assert "uptime" in data
    assert isinstance(data["uptime"], (int, float))
