from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load dataset
df = pd.read_csv("top_rated_2000webseries.csv")

@app.route("/overview", methods=["GET"])
def overview():
    return jsonify({
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "columns": [
            {"name": col, "dtype": str(df[col].dtype)}
            for col in df.columns
        ],
        "sample_data": df.head(5).to_dict(orient="records")
    })

if __name__ == "__main__":
    app.run(debug=True)
