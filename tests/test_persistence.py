import os
import tempfile
from app.persistence import write_last_city, read_last_city

def test_write_and_read_last_city(monkeypatch):
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name
    
    # Override DATA_PATH using monkeypatch
    monkeypatch.setenv("DATA_PATH", temp_path)

    # Write to the temp file
    write_last_city("Berlin")

    # Read from the temp file
    city = read_last_city()

    assert city == "Berlin"

    # Cleanup
    os.remove(temp_path)
