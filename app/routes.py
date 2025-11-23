from flask import Blueprint, render_template, request, jsonify, make_response
from .persistence import read_last_city, write_last_city

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """
    Serve the main HTML page for the Weather Dashboard.
    """
    return render_template("index.html")


@main_bp.route("/api/last-city", methods=["GET", "POST"])
def last_city():
    """
    GET  -> return the last saved city
    POST -> update the last saved city
    """
    if request.method == "GET":
        last_city = read_last_city()
        return make_response(jsonify({"last_city": last_city}), 200)

    # POST request
    payload = request.get_json(silent=True) or {}
    city = payload.get("last_city")

    if not city:
        return make_response(
            jsonify({"error": "last_city is required"}),
            400
        )

    write_last_city(city)

    return make_response(
        jsonify({"ok": True, "last_city": city}),
        200
    )
