@app.route("/predict_csv", methods=["POST"])
def predict_csv():

```
if "file" not in request.files:
    return jsonify({"error": "No file uploaded"}), 400

file = request.files["file"]

df = pd.read_csv(file)

# Remove Label column if present
if "Label" in df.columns:
    df = df.drop(columns=["Label"])

# Check for missing features
missing = [col for col in FEATURES if col not in df.columns]

if missing:
    return jsonify({
        "error": "Missing required features",
        "missing_columns": missing
    }), 400

# Keep only the features used during training
df = df[FEATURES]

predictions = model.predict(df)

return jsonify({
    "total_records": len(predictions),
    "predictions": predictions.tolist()
})
```
