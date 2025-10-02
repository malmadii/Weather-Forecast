# Weather-Forecast
A minimal, futuristic weather web app showing current conditions and a 7-day forecast for any city. Clean UI with hover effects and a personalized greeting. Uses Open-Meteo (free, no API key).

# Features
Current weather: temperature, condition text, icon
7-day forecast as hoverable bubbles (weekday, day/night temps, icon)
City search input
Personalized greeting (“Good morning/afternoon/evening, your name”) saved locally


#Tech Stack
Frontend: HTML, CSS, JS
Server: Python Flask (serves static files)
Data: Open-Meteo geocoding + forecast (no API key needed for this)

#How to quick start it
# 1) Clone
git clone https://github.com/malmadii/Weather-Forecast.git
cd <your-repo>

# 2) (Windows + Git Bash) create + activate venv
python -m venv venv
source venv/Scripts/activate

# 3) install & run
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000/


# Tip: After editing HTML/CSS/JS, hard refresh the browser (Ctrl+F5).
Stop the server with Ctrl+C in the terminal.


# Project Structure
app.py                  # minimal Flask server (serves index + static)
requirements.txt
templates/
  └─ index.html         # UI markup
static/
  ├─ style.css          # minimal/futuristic styling + hover animation for the 7 day forecast
  └─ app.js             # geocode + forecast + render


# How It Works
Browser loads index.html, style.css, and app.js from Flask.

app.js:
Geocodes the city via Open-Meteo
Fetches current + 7-day forecast (no key)
Renders the current card and 7 day bubbles
Saves your name to localStorage for the greeting
Icons: WMO weather codes are mapped to familiar icon codes (01d, 10d, …) and displayed via the OpenWeather icon CDN.

# Configuration: 
No API keys required.
