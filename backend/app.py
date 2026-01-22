from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

# Create Flask app FIRST
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load dataset
df = pd.read_csv("top_rated_2000webseries.csv")

@app.route("/")
def home():
    return "Flask backend is running"

@app.route("/overview")
def overview():
    return jsonify({
        "rows": int(df.shape[0]),
        "columns": list(df.columns)
    })

@app.route("/stats")
def stats():
    numeric = df.select_dtypes(include="number")

    # Remove ID-like columns (not statistically meaningful)
    if "id" in numeric.columns:
        numeric = numeric.drop(columns=["id"])

    desc = numeric.describe()

    cleaned = {}
    for col in desc.columns:
        cleaned[col] = {
            "mean": float(desc[col]["mean"]),
            "std": float(desc[col]["std"]),
            "min": float(desc[col]["min"]),
            "max": float(desc[col]["max"])
        }

    return jsonify(cleaned)


    # return jsonify(cleaned)

if __name__ == "__main__":
    app.run(debug=True)
