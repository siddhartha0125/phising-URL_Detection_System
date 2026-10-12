# Phishing URL Detection System

A beginner-friendly Flask web app that screens a submitted URL for common phishing warning signs.

## Requirements
- Python 3.10 or newer
- pip

## Run locally
1. Extract this folder.
2. Open a terminal in the project folder.
3. Create a virtual environment (recommended):
   - Windows: `py -m venv .venv`
   - Activate: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## Test examples
- `https://www.wikipedia.org` — likely to receive a low heuristic score.
- `http://192.0.2.10/login/verify-account` — should trigger several warning signs.
- `https://secure-login-account-example.com/verify` — may trigger suspicious-word/hyphen checks.

Use reserved/documentation IPs for testing, not real targets.

## Important limitations
This is an academic demonstration, not a production anti-phishing service. The score is a transparent checklist, not a trained or validated probability. A low score does not prove a site is safe, and a high score does not prove it is malicious. The app never visits submitted URLs, downloads content, or collects credentials. Do not deploy Flask's development server publicly. For real-world use, add a properly sourced and licensed dataset, train and evaluate a model, add rate limiting and logging safeguards, and use trusted threat-intelligence services carefully.
