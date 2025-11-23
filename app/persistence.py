import os
import json

# Default path to data.json (used in production)
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data.json"
)

def get_data_path() -> str:
    """
    Determine the path to the data.json file.
    Can be overridden by setting the DATA_PATH environment variable.
    This makes the function fully testable and CI-friendly.
    """
    return os.environ.get("DATA_PATH", DEFAULT_DATA_PATH)


def read_last_city() -> str:
    """
    Read the last saved city from data.json.
    Returns a default value ("Madrid") if the file doesn't exist
    or contains invalid JSON.
    """
    path = get_data_path()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("last_city", "Madrid")
    except Exception as e:
        # Logging helps debugging & monitoring
        print(f"[read_last_city] Failed to read data.json: {e}")
        return "Madrid"


def write_last_city(city: str) -> None:
    """
    Write the given city to data.json.
    Ensures the directory exists and handles write errors gracefully.
    """
    path = get_data_path()

    try:
        # Ensure the directory exists (important in Docker/CI)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump({"last_city": city}, f)

    except Exception as e:
        print(f"[write_last_city] Failed to write data.json: {e}")
