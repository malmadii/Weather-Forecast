# Weather Dashboard

A lightweight weather web application that displays the current weather and a 7-day forecast for any city.  
The project is built with Flask (using an application factory + blueprints) and a simple HTML/CSS/JS frontend.  
Weather data is fetched from Open-Meteo, which requires no API key.  

The application is fully containerized with Docker and deployed to Azure App Service using an automated CI/CD pipeline powered by GitHub Actions.

**Live App Deployment:**  
https://weather-dashboard-mona-cva6eagagxacatek.westeurope-01.azurewebsites.net/

**Metrics** 
https://weather-dashboard-mona-cva6eagagxacatek.westeurope-01.azurewebsites.net/metrics 


# Features

- Current weather: temperature, condition description, icon
- 7-day forecast displayed as interactive bubble cards
- City search with basic error handling
- Personalized greeting stored in localStorage
- Persistent “last searched city” stored in `data.json` via Flask
- `/health` endpoint for container ready checks
- `/metrics` endpoint exposing Prometheus metrics directly from Flask

---

# Tech Stack

**Frontend:**  
- HTML  
- CSS  
- Vanilla JavaScript  

**Backend:**  
- Python Flask  
- Blueprints  
- Application factory (`create_app()`)  

**APIs:**  
- Open-Meteo Geocoding  
- Open-Meteo Forecast  

**DevOps:**  
- GitHub Actions (CI + CD)  
- Docker  
- Azure Web App for Containers  
- Prometheus client library for metrics

---

# Local Development

### 1. Clone

```bash
git clone https://github.com/malmadii/Weather-Forecast.git
cd Weather-Forecast

### 2) Create & activate virtual environment (Windows + Git Bash)

```bash
python -m venv venv
source venv/Scripts/activate


### 3) Install dependencies & run the server

```bash
pip install -r requirements.txt
python app.py

### 4) Open in browser
http://127.0.0.1:5000/


##Project Structure
app/
  __init__.py           # Flask application factory
  routes.py             # UI + /api/last-city
  persistence.py        # JSON-based storage
  monitoring.py         # /health + /metrics (Prometheus)

tests/
  test_routes.py
  test_persistence.py
  test_health.py

templates/
  index.html

static/
  style.css
  app.js

Dockerfile
ci.yml                  # CI workflow
cd.yml                  # CD workflow
requirements.txt
data.json
app.py                  # Local entrypoint

# How It Works

### Frontend (no API keys required)

`app.js` handles:

- city search  
- geocoding → coordinates  
- fetching 7-day + current forecast  
- rendering weather cards  
- storing greeting in `localStorage`  
- saving last city via POST to Flask  

---

### Backend

`routes.py` exposes:

- `GET /api/last-city` → retrieves last stored city  
- `POST /api/last-city` → saves the new one  
- `GET /` → serves the frontend  

---

### Persistence

`persistence.py` reads/writes from `data.json`.  
During tests, the file path is overridden using environment variables so that real user data is never modified.

---

# Monitoring & Prometheus Metrics

### Health Check: `/health`

Flask returns a simple status and uptime value:

```json
{ "status": "ok", "uptime": 14.52 }

### Used by:

- Docker `HEALTHCHECK`
- Azure startup checks

---

### Prometheus Metrics: `/metrics`

The complete Prometheus setup is implemented in `monitoring.py` and includes:

- **weather_app_requests_total** — total request count  
- **weather_app_request_latency_seconds** — request latency histogram  
- **weather_app_errors_total** — 4xx/5xx error counter  

Every request is automatically tracked through Flask’s  
`before_app_request` and `after_app_request` hooks.

No additional setup is required.  
To view metrics, open:

https://weather-dashboard-mona-cva6eagagxacatek.westeurope-01.azurewebsites.net/metrics


Prometheus-formatted metrics will be displayed.


# Testing

Run all tests:

```bash
pytest -q


## Troubleshooting

App won’t start on Azure:

- ensure container binds to port 8000

- check Azure “Log Stream” for runtime errors

- confirm create_app() exists and all blueprints register correctly

Metrics not showing:

- check /health to confirm the container is running

- restart the app from Azure Portal

Persistence issues:

- verify data.json exists and is writable

- inspect GET/POST requests in browser DevTools
