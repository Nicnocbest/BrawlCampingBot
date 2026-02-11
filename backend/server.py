from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

FILE = "completed.json"

# create file if missing
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


def load():
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================
# LINKVERTISE REDIRECT ENDPOINT
# ============================
@app.route("/complete")
def complete():
    user = request.args.get("user")

    if not user:
        return "❌ Missing username", 400

    data = load()

    if user not in data:
        data.append(user)
        save(data)

    return "✅ Completed! Go back to Telegram and type /claim"


# ============================
# BOT CHECK ENDPOINT (ONE TIME)
# ============================
@app.route("/check", methods=["POST"])
def check():
    username = request.json.get("username")
    data = load()

    if username in data:
        # remove user after successful claim
        data.remove(username)
        save(data)

        return jsonify({"verified": True})

    return jsonify({"verified": False})


# ============================
# RUN
# ============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)