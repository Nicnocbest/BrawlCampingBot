import requests
import sys

API_URL = "http://127.0.0.1:5000/validate-key"


def check_license():
    try:
        with open("license.key", "r") as f:
            key = f.read().strip()
    except:
        print("❌ No license.key file found!")
        sys.exit()

    if key == "" or key == "PASTE-YOUR-KEY-HERE":
        print("❌ No valid key inside license.key")
        sys.exit()

    try:
        response = requests.post(API_URL, json={"key": key})
        data = response.json()

        if not data.get("valid"):
            print("❌ Key invalid or expired!")
            sys.exit()

        print("✅ License Key Valid. Starting bot...")

    except Exception as e:
        print("❌ Could not connect to license server!")
        sys.exit()
