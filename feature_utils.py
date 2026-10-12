"""Educational URL feature extraction and classification utilities.
The app analyzes the URL string only; it does not open or request the destination website.
"""
from urllib.parse import urlparse
import ipaddress
import re
import math

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly",
    "buff.ly", "cutt.ly", "rb.gy", "shorturl.at"
}
SUSPICIOUS_WORDS = {
    "login", "verify", "update", "secure", "account", "password",
    "signin", "confirm", "wallet", "banking", "payment", "recover"
}

def normalize_url(raw_url: str) -> str:
    value = raw_url.strip()
    if not value:
        raise ValueError("Enter a URL.")
    if any(ch.isspace() for ch in value):
        raise ValueError("The URL must not contain spaces.")
    if "://" not in value:
        value = "http://" + value
    parsed = urlparse(value)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs can be analyzed.")
    if not parsed.hostname:
        raise ValueError("The URL does not contain a valid hostname.")
    return value

def extract_features(raw_url: str) -> dict:
    url = normalize_url(raw_url)
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path_query = (parsed.path + "?" + parsed.query).lower()
    try:
        ipaddress.ip_address(host)
        has_ip = 1
    except ValueError:
        has_ip = 0
    labels = host.split(".")
    return {
        "url_length": len(url),
        "host_length": len(host),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "digit_count": sum(ch.isdigit() for ch in url),
        "subdomain_count": max(0, len(labels) - 2),
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_ip_address": has_ip,
        "has_port": int(parsed.port is not None) if parsed.port else 0,
        "has_double_slash_path": int("//" in parsed.path),
        "has_encoded_chars": int("%" in url),
        "has_suspicious_word": int(any(word in path_query or word in host for word in SUSPICIOUS_WORDS)),
        "uses_shortener": int(host in SHORTENERS),
        "has_punycode": int("xn--" in host),
        "query_parameter_count": len([p for p in parsed.query.split("&") if p]) if parsed.query else 0,
    }

def heuristic_score(features: dict) -> tuple[int, list[str]]:
    score = 0
    reasons = []
    def add(condition, points, message):
        nonlocal score
        if condition:
            score += points
            reasons.append(message)
    add(features["has_ip_address"] == 1, 22, "The hostname is an IP address instead of a normal domain.")
    add(features["at_count"] > 0, 18, "The URL contains an @ symbol, which can disguise the destination.")
    add(features["uses_shortener"] == 1, 12, "The domain is a known URL-shortening service.")
    add(features["has_punycode"] == 1, 18, "The domain contains punycode, which can be used in look-alike domains.")
    add(features["uses_https"] == 0, 8, "The URL does not use HTTPS.")
    add(features["url_length"] > 100, 10, "The URL is unusually long.")
    add(features["subdomain_count"] >= 3, 10, "The hostname contains many subdomain labels.")
    add(features["hyphen_count"] >= 3, 7, "The URL contains several hyphens.")
    add(features["has_suspicious_word"] == 1, 8, "The URL contains words often used in account or login lures.")
    add(features["digit_count"] >= 7, 5, "The URL contains many digits.")
    add(features["has_encoded_chars"] == 1, 3, "The URL contains percent-encoded characters.")
    score = min(score, 100)
    if not reasons:
        reasons.append("No high-risk pattern from this small heuristic checklist was detected.")
    return score, reasons

def classify_url(raw_url: str) -> dict:
    normalized = normalize_url(raw_url)
    features = extract_features(normalized)
    score, reasons = heuristic_score(features)
    # Labels are screening guidance, not a definitive verdict.
    label = "Suspicious" if score >= 30 else "Potentially Safe"
    confidence_note = (
        "This is a lightweight educational heuristic score, not a probability or a guarantee."
    )
    return {
        "url": normalized,
        "label": label,
        "score": score,
        "reasons": reasons,
        "features": features,
        "confidence_note": confidence_note,
    }
