from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FILE = "completed.json"


# =========================
# INIT FILE
# =========================
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


def load_tokens():
    with open(FILE, "r") as f:
        return json.load(f)


def save_tokens(tokens):
    with open(FILE, "w") as f:
        json.dump(tokens, f, indent=2)


# =========================
# LINKVERTISE COMPLETION
# =========================
@app.route("/complete")
def complete():
    token = request.args.get("token")

    if not token:
        return "❌ Missing token", 400

    tokens = load_tokens()

    if token not in tokens:
        tokens.append(token)
        save_tokens(tokens)

    return f"""
    ✅ Linkvertise Completed!<br><br>
    Now go back to Telegram and type:<br><br>
    <b>/claim {token}</b>
    """


# =========================
# BOT CHECK TOKEN
# =========================
@app.route("/check", methods=["POST"])
def check():
    data = request.json
    token = data.get("token")

    tokens = load_tokens()

    # ❌ Token not completed
    if token not in tokens:
        return jsonify({"ok": False}), 403

    # ✅ Token valid → remove (1-time use)
    tokens.remove(token)
    save_tokens(tokens)

    return jsonify({"ok": True})


# =========================
# HOME (OPTIONAL)
# =========================
@app.route("/")
def home():
    return "✅ BrawlStarsAutoplay Backend Running"


# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)