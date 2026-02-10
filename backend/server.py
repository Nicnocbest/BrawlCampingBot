VERIFIED_FILE = "verified_users.json"

def load_verified():
    if not os.path.exists(VERIFIED_FILE):
        return []
    with open(VERIFIED_FILE, "r") as f:
        return json.load(f)

def save_verified(users):
    with open(VERIFIED_FILE, "w") as f:
        json.dump(users, f, indent=2)


@app.route("/verify-user", methods=["POST"])
def verify_user():
    data = request.json
    username = data.get("username", "").strip()

    users = load_verified()

    if username not in users:
        users.append(username)
        save_verified(users)

    return jsonify({"status": "verified"})
