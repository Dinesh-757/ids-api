from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

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

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    return jsonify({
        "prediction": str(prediction)
    })

if __name__ == "__main__":
    app.run()
