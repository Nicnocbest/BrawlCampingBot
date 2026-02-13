from flask import Flask, request, jsonify
import json
import os
import random
import string

app = Flask(__name__)

TOKENS_FILE = "completed_tokens.json"


# ==========================
# INIT FILE
# ==========================

if not os.path.exists(TOKENS_FILE):
    with open(TOKENS_FILE, "w") as f:
        json.dump({}, f)


def load_tokens():
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)


def save_tokens(data):
    with open(TOKENS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_token():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


# ==========================
# HOME
# ==========================

@app.route("/")
def home():
    return "✅ Backend Running"


# ==========================
# LINKVERTISE COMPLETE
# ==========================

@app.route("/complete")
def complete():
    tokens = load_tokens()

    token = generate_token()

    tokens[token] = False  # False = unused
    save_tokens(tokens)

    return f"""
    <h2>✅ Linkvertise Completed!</h2>
    <p>Now go back to Telegram and type:</p>
    <h3>/claim {token}</h3>
    """


# ==========================
# CHECK TOKEN
# ==========================

@app.route("/check")
def check():
    token = request.args.get("token")

    if not token:
        return jsonify({"completed": False})

    tokens = load_tokens()

    # Token not found
    if token not in tokens:
        return jsonify({"completed": False})

    # Already used
    if tokens[token] is True:
        return jsonify({"completed": False})

    # Mark as used
    tokens[token] = True
    save_tokens(tokens)

    return jsonify({"completed": True})


# ==========================
# RUN LOCAL
# ==========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
