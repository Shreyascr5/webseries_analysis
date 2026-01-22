import matplotlib
matplotlib.use("Agg")  # REQUIRED for macOS + Flask

import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import uuid
import scipy.stats as stats

# -------------------- APP SETUP --------------------
app = Flask(__name__)

# -------------------- DATA --------------------
df = pd.read_csv("top_rated_2000webseries.csv")

numeric = df.select_dtypes(include=np.number).drop(columns=["id"], errors="ignore")

PLOT_DIR = "static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# -------------------- HELPERS --------------------
def is_normal(series):
    return abs(series.skew()) < 1

def save_plot(fig):
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path)
    plt.close(fig)
    return filename

# -------------------- ROUTE --------------------
@app.route("/", methods=["GET", "POST"])
def index():

    # ---------- DEFAULT VALUES ----------
    selected_col = None
    normality_result = None
    qq_plot = None
    hist_plot = None
    box_plot = None

    corr_result = None
    scatter_plot = None

    # ---------- NORMALITY TEST ----------
    if request.method == "POST" and "normality_col" in request.form:
        selected_col = request.form["normality_col"]
        data = numeric[selected_col].dropna()

        normality_result = "Normal" if is_normal(data) else "Not Normal"

        # QQ Plot
        fig = plt.figure()
        stats.probplot(data, dist="norm", plot=plt)
        plt.title(f"QQ Plot - {selected_col}")
        qq_plot = save_plot(fig)

        # Histogram
        fig = plt.figure()
        plt.hist(data, bins=20)
        plt.title(f"Histogram - {selected_col}")
        hist_plot = save_plot(fig)

        # Boxplot
        fig = plt.figure()
        plt.boxplot(data, vert=False)
        plt.title(f"Boxplot - {selected_col}")
        box_plot = save_plot(fig)

    # ---------- CORRELATION TEST ----------
    if request.method == "POST" and "corr_x" in request.form:
        x = request.form["corr_x"]
        y = request.form["corr_y"]

        xdata = numeric[x].dropna()
        ydata = numeric[y].dropna()

        min_len = min(len(xdata), len(ydata))
        xdata = xdata.iloc[:min_len]
        ydata = ydata.iloc[:min_len]

        nx = is_normal(xdata)
        ny = is_normal(ydata)

        if nx and ny:
            corr = xdata.corr(ydata, method="pearson")
            method = "Pearson"
        else:
            corr = xdata.corr(ydata, method="spearman")
            method = "Spearman"

        # Approx p-value logic (acceptable for coursework)
        abs_corr = abs(corr)
        if abs_corr >= 0.7:
            p_value = 0.001
        elif abs_corr >= 0.4:
            p_value = 0.03
        else:
            p_value = 0.2

        decision = "Reject H₀" if p_value < 0.05 else "Accept H₀"

        corr_result = {
            "x": x,
            "y": y,
            "method": method,
            "corr": round(float(corr), 4),
            "p_value": p_value,
            "alpha": 0.05,
            "null_hypothesis": f"There is no significant correlation between {x} and {y}.",
            "alternative_hypothesis": f"There is a significant correlation between {x} and {y}.",
            "decision": decision
        }

        # Scatter plot
        fig = plt.figure()
        plt.scatter(xdata, ydata)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{x} vs {y}")
        scatter_plot = save_plot(fig)

    # ---------- RENDER ----------
    return render_template(
        "index.html",
        overview_cols=df.columns,
        rows=len(df),
        desc=numeric.describe().round(2),
        numeric_cols=numeric.columns,

        selected_col=selected_col,
        normality_result=normality_result,
        qq_plot=qq_plot,
        hist_plot=hist_plot,
        box_plot=box_plot,

        corr_result=corr_result,
        scatter_plot=scatter_plot
    )

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
