from flask import Flask, render_template, request
from urllib.parse import urlparse
import ipaddress
import re
import math
from feature_utils import extract_features, heuristic_score, classify_url

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    submitted_url = ""
    error = None
    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()
        if not submitted_url:
            error = "Please enter a URL to analyze."
        elif len(submitted_url) > 2048:
            error = "The URL is too long to analyze."
        else:
            try:
                result = classify_url(submitted_url)
            except ValueError as exc:
                error = str(exc)
    return render_template("index.html", result=result, submitted_url=submitted_url, error=error)

if __name__ == "__main__":
    # Local educational demo only. Do not expose Flask's development server publicly.
    app.run(debug=True)
