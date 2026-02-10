from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
import string
from datetime import datetime, timedelta

# =========================
# APP SETUP
# =========================
app = Flask(__name__)
CORS(app)  # ✅ Allow website requests (Fix for browser blocking)

# =========================
# FILE PATHS
# =========================
VERIFIED_FILE = "../telegram/verified_users.json"
KEYS_FILE = "keys.json"


# =========================
# LOAD VERIFIED USERS
# =========================
def load_verified_users():
    if not os.path.exists(VERIFIED_FILE):
        return []

    try:
        with open(VERIFIED_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# =========================
# LOAD + SAVE KEYS
# =========================
def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}

    try:
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=2)


# =========================
# GENERATE RANDOM KEY
# =========================
def generate_key():
    return "BS-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=16)
    )


# =========================
# API ROUTE: GENERATE KEY
# =========================
@app.route("/generate-key", methods=["POST"])
def generate_key_route():
    data = request.json
    username = data.get("username", "").strip()

    if username == "":
        return jsonify({"error": "No username provided"}), 400

    verified_users = load_verified_users()

    # Check if user is verified
    if username not in verified_users:
        return jsonify({"error": "User not verified. Verify in Telegram first."}), 403

    keys = load_keys()

    # Generate key valid for 24 hours
    key = generate_key()
    expires = (datetime.utcnow() + timedelta(hours=24)).isoformat()

    keys[key] = {
        "username": username,
        "expires": expires
    }

    save_keys(keys)

    return jsonify({
        "status": "success",
        "key": key,
        "expires": expires
    })


# =========================
# API ROUTE: VALIDATE KEY
# =========================
@app.route("/validate-key", methods=["POST"])
def validate_key_route():
    data = request.json
    key = data.get("key", "").strip()

    keys = load_keys()

    if key not in keys:
        return jsonify({"valid": False})

    expires = datetime.fromisoformat(keys[key]["expires"])

    if datetime.utcnow() > expires:
        return jsonify({"valid": False, "reason": "expired"})

    return jsonify({"valid": True})


# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    print("✅ Backend running at: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
