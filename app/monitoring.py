from flask import Blueprint, jsonify, request
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

monitoring_bp = Blueprint("monitoring", __name__)

# Application uptime
start_time = time.time()

# -------------------------
# Prometheus Metrics
# -------------------------

# Total number of requests
REQUEST_COUNT = Counter(
    "weather_app_requests_total",
    "Total HTTP requests received",
    ["method", "endpoint"]
)

# Request latency histogram
REQUEST_LATENCY = Histogram(
    "weather_app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)

# Error counter
ERROR_COUNT = Counter(
    "weather_app_errors_total",
    "Total number of HTTP errors",
    ["endpoint", "status"]
)


# -------------------------
# Hooks for automatically tracking metrics
# -------------------------

@monitoring_bp.before_app_request
def before_request():
    """
    Store the start time of the request so latency can be measured later.
    """
    request.start_time = time.time()


@monitoring_bp.after_app_request
def after_request(response):
    """
    After each request:
    - increment request counter
    - record latency
    - count errors (4xx, 5xx)
    """
    endpoint = request.endpoint or "unknown"

    # Count every request
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()

    # Measure latency
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

    # Count errors
    if response.status_code >= 400:
        ERROR_COUNT.labels(endpoint=endpoint, status=response.status_code).inc()

    return response


# -------------------------
# Health endpoint
# -------------------------

@monitoring_bp.route("/health")
def health():
    """
    Basic health check used by deployment platforms and monitoring systems.
    """
    uptime = round(time.time() - start_time, 2)
    return jsonify({"status": "ok", "uptime": uptime})


# -------------------------
# Metrics endpoint
# -------------------------

@monitoring_bp.route("/metrics")
def metrics():
    """
    Exposes Prometheus-formatted application metrics.
    """
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
