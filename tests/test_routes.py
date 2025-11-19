import os
import tempfile
from app import create_app

def test_post_last_city(monkeypatch):
    app = create_app()
    client = app.test_client()

    # Temporary test file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    monkeypatch.setenv("DATA_PATH", temp_path)

    res = client.post("/api/last-city", json={"last_city": "Tokyo"})

    assert res.status_code == 200
    assert res.json["last_city"] == "Tokyo"

    os.remove(temp_path)
