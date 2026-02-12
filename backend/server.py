from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

FILE = "completed_tokens.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


def load():
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/complete")
def complete():
    token = request.args.get("token")

    if not token:
        return "❌ Missing token", 400

    data = load()

    if token not in data:
        data.append(token)
        save(data)

    return "✅ Completed! Go back to Telegram and type:\n/claim YOURTOKEN"


@app.route("/check", methods=["POST"])
def check():
    token = request.json.get("token")
    data = load()

    if token in data:
        data.remove(token)
        save(data)
        return jsonify({"verified": True})

    return jsonify({"verified": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)