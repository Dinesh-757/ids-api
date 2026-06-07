from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np.0", port=10000)
@app.route("/predict_csv", methods=["POST"])
def predict_csv():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        import numpy as np

        file = request.files["file"]

        df = pd.read_csv(file)

        # Remove Label column if present
        if "Label" in df.columns:
            df = df.drop(columns=["Label"])

        # Match the exact features used during training
        if FEATURES:
            missing = [col for col in FEATURES if col not in df.columns]

            if missing:
                return jsonify({
                    "error": "Missing required columns",
                    "missing_columns": missing
                }), 400

            df = df[FEATURES]

        # Replace Infinity values
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Replace NaN values
        df.fillna(0, inplace=True)

        # Limit extremely large values
        df = df.clip(-1e9, 1e9)

        # Convert to float32
        df = df.astype("float32")

        predictions = model.predict(df)

        return jsonify({
            "total_records": len(predictions),
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
