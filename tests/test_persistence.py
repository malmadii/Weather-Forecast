import os
import json
import tempfile
import pytest

from app.persistence import write_last_city, read_last_city


@pytest.fixture
def temp_data_file(monkeypatch):
    """
    Creates a temporary file and sets DATA_PATH to point to it.
    Ensures persistence tests never touch the real data.json.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    monkeypatch.setenv("DATA_PATH", temp_path)

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


# --------------------------------------------------------
# TEST: Basic write → read flow
# --------------------------------------------------------
def test_write_and_read_last_city(temp_data_file):
    """write_last_city should store the city, and read_last_city should retrieve it."""
    
    # Arrange
    write_last_city("Berlin")

    # Act
    result = read_last_city()

    # Assert
    assert result == "Berlin"


# --------------------------------------------------------
# TEST: read_last_city returns default when file missing
# --------------------------------------------------------
def test_read_last_city_defaults_when_file_missing(monkeypatch):
    """If data file doesn't exist, read_last_city should return the default ('Madrid')."""
    
    monkeypatch.setenv("DATA_PATH", "nonexistent_file_123.json")

    result = read_last_city()
    assert result == "Madrid"


# --------------------------------------------------------
# TEST: read_last_city handles corrupted JSON safely
# --------------------------------------------------------
def test_read_last_city_with_corrupted_json(temp_data_file):
    """Corrupted JSON should not crash and should return the default value."""

    # Write corrupted data to the temp file
    with open(temp_data_file, "w", encoding="utf-8") as f:
        f.write("{ invalid json")

    # Act
    result = read_last_city()

    # Assert
    assert result == "Madrid"


# --------------------------------------------------------
# TEST: write_last_city overwrites the existing value
# --------------------------------------------------------
def test_write_overwrites_existing_city(temp_data_file):
    """Second write should overwrite the previous stored city."""

    write_last_city("Rome")
    write_last_city("Tokyo")

    result = read_last_city()
    assert result == "Tokyo"
