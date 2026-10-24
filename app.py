
from flask import Flask, request, jsonify
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Demo ML model: trained on synthetic data only.
# This is not a real-world blood shortage forecasting model.
rng = np.random.default_rng(42)

rates = np.linspace(0, 100, 1001).reshape(-1, 1)
labels = np.where(
    rates[:, 0] < 50, 2,
    np.where(rates[:, 0] < 70, 1, 0)
)

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(rates, labels)

LABEL_NAMES = {
    2: "High Concern",
    1: "Moderate Concern",
    0: "Lower Concern"
}

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/")
def home():
    return jsonify({
        "project": "BloodLink AI",
        "status": "Backend working",
        "ml_model": "Demo Decision Tree",
        "real_world_validated": False
    })

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}

    try:
        total = int(data.get("total", 0))
        available = int(data.get("available", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid numbers"}), 400

    if total <= 0 or available < 0 or available > total:
        return jsonify({"error": "Invalid data"}), 400

    rate = round(available / total * 100, 2)

    prediction = int(model.predict([[rate]])[0])
    level = LABEL_NAMES[prediction]

    return jsonify({
        "availability_rate": rate,
        "shortage_indicator": level,
        "model_type": "Demo Decision Tree",
        "demo_model": True
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
