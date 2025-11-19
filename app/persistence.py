import os
import json

# Default path for production
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data.json"
)

def get_data_path():
    """
    Allows overriding the data.json path using an environment variable.
    This is critical for testing because tests must not modify real data.json.
    """
    return os.environ.get("DATA_PATH", DEFAULT_DATA_PATH)

def read_last_city():
    path = get_data_path()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("last_city", "Madrid")
    except Exception:
        return "Madrid"

def write_last_city(city):
    path = get_data_path()

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_city": city}, f)
