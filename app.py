from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load("ids_model.pkl")

try:
    FEATURES = list(model.feature_names_in_)
except:
    FEATURES = []

@app.route("/")
def home():
    return "IDS Prediction API is running"

@app.route("/features")
def features():
    return jsonify({
        "feature_count": len(FEATURES),
        "features": FEATURES
    })

@app.route("/predict_csv", methods=["POST"])
def predict_csv():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    df = pd.read_csv(file)

    predictions = model.predict(df)

    return jsonify({
        "total_records": len(predictions),
        "predictions": predictions.tolist()
    })

if __name__ == "__main__":
    app.run()
