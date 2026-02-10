from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import json
import os

# =========================
# CONFIG
# =========================
TOKEN = "8102080453:AAFzlsvyPT5SinF7xeupONxS4XxvG9M9zYg"
WEBSITE_LINK = "https://brawlstars-autoplay.wuaze.com/index.html"

DATA_FILE = "verified_users.json"


# =========================
# INITIALIZE FILE
# =========================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


# =========================
# LOAD + SAVE USERS
# =========================
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()

            if content == "":
                return []

            return json.loads(content)

    except Exception:
        return []


def save_user(username):
    users = load_users()

    if username not in users:
        users.append(username)

    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)


# =========================
# COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "This bot is for the BrawlStars Camping Bot project.\n\n"
        f"🌍 Website: {WEBSITE_LINK}\n\n"
        "To verify yourself, use:\n"
        "/link"
    )


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ Please send your Telegram username now.\n"
        "Without @\n\n"
        "Example:\n"
        "nici123"
    )

    context.user_data["awaiting_username"] = True


# =========================
# USER INPUT HANDLER
# =========================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("awaiting_username"):
        return

    username = update.message.text.strip()

    save_user(username)

    await update.message.reply_text(
        f"✅ Username '{username}' has been verified!\n\n"
        "You can now get your key from the website."
    )

    context.user_data["awaiting_username"] = False


# =========================
# MAIN
# =========================
def main():
    print("🤖 Telegram bot is starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("link", link))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
