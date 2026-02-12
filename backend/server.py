from flask import Flask
import json
import random
import string
import os

app = Flask(__name__)

TOKENS_FILE = "completed.json"

# ============================
# INIT TOKEN STORAGE
# ============================
if not os.path.exists(TOKENS_FILE):
    with open(TOKENS_FILE, "w") as f:
        json.dump({}, f)


# ============================
# CREATE RANDOM TOKEN
# ============================
def create_token():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


# ============================
# SAVE TOKEN
# ============================
def save_token(token):
    with open(TOKENS_FILE, "r") as f:
        data = json.load(f)

    data[token] = False  # False = not used yet

    with open(TOKENS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================
# COMPLETE LINKVERTISE
# ============================
@app.route("/complete")
def complete():
    token = create_token()
    save_token(token)

    return f"""
    <h2>✅ Linkvertise Completed!</h2>
    <p>Now go back to Telegram and type:</p>
    <h3>/claim {token}</h3>
    """


# ============================
# CHECK TOKEN VALID
# ============================
@app.route("/check/<token>")
def check_token(token):
    with open(TOKENS_FILE, "r") as f:
        data = json.load(f)

    if token not in data:
        return {"valid": False}

    if data[token] is True:
        return {"valid": False}

    # mark as used
    data[token] = True
    with open(TOKENS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return {"valid": True}


# ============================
# RUN SERVER
# ============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)