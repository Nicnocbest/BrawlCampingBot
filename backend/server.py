from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

FILE = "completed.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


def load_tokens():
    with open(FILE, "r") as f:
        return json.load(f)


def save_tokens(tokens):
    with open(FILE, "w") as f:
        json.dump(tokens, f, indent=2)


@app.route("/complete")
def complete():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400

    tokens = load_tokens()

    if token not in tokens:
        tokens.append(token)
        save_tokens(tokens)

    return "✅ Completed! Go back to Telegram and type /claim"


@app.route("/check", methods=["POST"])
def check():
    data = request.json
    token = data.get("token")

    tokens = load_tokens()

    if token not in tokens:
        return jsonify({"ok": False}), 403

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run()