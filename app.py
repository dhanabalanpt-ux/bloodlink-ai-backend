from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "project": "BloodLink AI",
        "status": "Backend working"
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}

    try:
        total = int(data.get("total", 0))
        available = int(data.get("available", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid numbers"}), 400

    if total <= 0 or available < 0 or available > total:
        return jsonify({"error": "Invalid data"}), 400

    rate = round(available / total * 100, 2)

    if rate < 50:
        level = "High Concern"
    elif rate < 70:
        level = "Moderate Concern"
    else:
        level = "Lower Concern"

    return jsonify({
        "availability_rate": rate,
        "shortage_indicator": level
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
