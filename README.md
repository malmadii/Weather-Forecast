# Weather Dashboard

A minimal, futuristic weather web app showing current conditions and a 7-day forecast for any city. Clean “bubble” UI with hover effects, a personalized greeting, and no API key (uses Open-Meteo).
Now also remembers your last searched city via a tiny REST endpoint and data.json.

# Features

1) Current weather: temperature, condition text, icon

2) 7-day forecast as hoverable bubbles (weekday, day & night temps, icon)

3) City search input

4) Personalized greeting (“Good morning/afternoon/evening, your name”) saved in the browser (localStorage)

5) Persistence: remembers the last searched city across page reloads (file-based via Flask)

 # Tech Stack

Frontend: HTML, CSS, Vanilla JS

Server: Python Flask (serves the page + tiny REST endpoint)

Weather Data: Open-Meteo Geocoding & Forecast (no API key)

# Quick Start
# 1) clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2) (Windows + Git Bash) create & activate venv
python -m venv venv
source venv/Scripts/activate

# 3) install & run
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000/


Tip: After editing HTML/CSS/JS, Ctrl+F5 (hard refresh) to see changes.

# Project Structure
app.py                  # Flask server (serves UI + /api/last-city)
requirements.txt
data.json               # simple persistence: { "last_city": "..." }
templates/
  └─ index.html         # UI markup
static/
  ├─ style.css          # minimal/futuristic styling + hover
  └─ app.js             # Open-Meteo fetches + render + persistence calls

# How It Works
Frontend (no keys needed)

User enters a city → app.js:

Geocodes city via Open-Meteo

Fetches current + 7-day forecast

Renders a current card and 7 day bubbles

Personalized greeting is stored in localStorage.

After a successful search, the city is saved via a small REST call to Flask.

Persistence (new)

GET /api/last-city → returns { "last_city": "<city>" } (from data.json)

POST /api/last-city with { "last_city": "<city>" } → updates data.json

On page load, the UI loads the last city and renders it automatically.

# Endpoints (for reference)

GET / — serves the app (index.html)

GET /api/last-city — returns the last saved city

POST /api/last-city — saves { "last_city": "Paris" }

# Architecture
Browser (HTML/CSS/JS)
  ├─ City input + Greeting (localStorage)
  ├─ Fetch Open-Meteo Geocoding
  └─ Fetch Open-Meteo Forecast (current + daily)
          │
          ▼
   Open-Meteo APIs (no key)

Flask (app.py)
  ├─ serves index.html, CSS, JS
  └─ /api/last-city (GET/POST) -> data.json

# Manual Test Checklist

Search a valid city → current card + 7 bubbles appear quickly

Hover a bubble → slight enlarge animation

Misspell a city → friendly error alert

Change your name → greeting updates & persists

Refresh the page → last searched city loads automatically

# Troubleshooting

Blank UI / -- values: open DevTools → Network; verify requests to geocoding-api.open-meteo.com and api.open-meteo.com return 200.

City not found: try a different spelling (“New York”, “São Paulo”).

Persistence not working: check GET /api/last-city in the browser; ensure data.json exists and is writable.

# Configuration & Git Hygiene

No API keys required.
.gitignore:

venv/
.venv/
__pycache__/
*.pyc
.env

# Roadmap (next steps)

Loading states & inline error toasts

“Use my location” (geolocation + reverse geocode via server proxy)

Light/dark theme toggle

Tests (unit/integration/UI), Dockerfile, GitHub Actions CI

Optional switch to OpenWeather (proxy via Flask + .env secret)
