import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("API_KEY loaded? ->", bool(API_KEY))
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Madrid")

app = Flask(__name__)

@app.route("/")
def index():
    # Home page renders the template; JS will call our API
    return render_template("index.html", greeting="Good Morning")

def fetch_current_weather(city: str):
    """
    Use OpenWeather 'current weather' endpoint (simple to start).
    Returns dict with: city, temp (°C), description, icon.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code == 401:
        return {"error": "Invalid or inactive API key (401). Wait a few minutes after creating it and verify email."}
    if r.status_code == 404:
        return {"error": f"City '{city}' not found."}
    r.raise_for_status()
    data = r.json()
    name = data.get("name", city)
    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]
    icon = weather.get("icon", "01d")
    description = weather.get("description", "").title()

    return {
        "city": name,
        "temp": round(main.get("temp", 0)),
        "description": weather.get("description", "").title(),
        "icon": weather.get("icon", "01d")
    }

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city") or DEFAULT_CITY
    try:
        return jsonify(fetch_current_weather(city))
    except requests.RequestException as e:
        return jsonify({"error": f"Network/API error: {e}"}), 502
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
