from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(**name**)
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

```
if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400

try:
    file = request.files["file"]

    df = pd.read_csv(file)

    # Remove Label column if present
    if "Label" in df.columns:
        df = df.drop(columns=["Label"])

    # Keep only training features
    if FEATURES:
        missing = [col for col in FEATURES if col not in df.columns]

        if missing:
            return jsonify({
                "error": "Missing required columns",
                "missing_columns": missing
            }), 400

        df = df[FEATURES]

    # Clean problematic values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    # Prevent extremely large values
    df = df.clip(-1e9, 1e9)

    predictions = model.predict(df)

    return jsonify({
        "total_records": len(predictions),
        "predictions": predictions.tolist()
    })

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

if **name** == "**main**":
app.run(debug=True)
