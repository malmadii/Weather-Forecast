from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# --- simple file persistence for "last searched city" ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def read_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_city": "Madrid"}  # default

def write_data(obj):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(obj, f)

@app.route("/")
def index():
    return render_template("index.html")

# GET -> {"last_city": "..."} | POST -> save {"last_city": "..."}
@app.route("/api/last-city", methods=["GET", "POST"])
def last_city():
    if request.method == "GET":
        return jsonify(read_data())

    payload = request.get_json(silent=True) or {}
    city = payload.get("last_city")
    if not city:
        return jsonify({"error": "last_city is required"}), 400

    data = read_data()
    data["last_city"] = city
    write_data(data)
    return jsonify({"ok": True, "last_city": city})

if __name__ == "__main__":
    app.run(debug=True)
