import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *Welcome to FF Ban Check Bot*\n\n"
        "👉 Enter your *Free Fire UID* to check ban status.",
        parse_mode="Markdown"
    )

# Handle UID input
async def check_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()

    if not uid.isdigit():
        await update.message.reply_text("❌ Please enter a valid numeric UID")
        return

    url = f"https://krsxh-ban-check.vercel.app/check/{uid}"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if data.get("success"):
            status = data.get("status")
            is_banned = data.get("is_banned")
            reason = data.get("reason") or "No reason"
            period = data.get("period")

            msg = (
                f"🎮 *Free Fire Ban Status*\n\n"
                f"🆔 UID: `{uid}`\n"
                f"📌 Status: *{status}*\n"
                f"🚫 Banned: *{is_banned}*\n"
                f"⏳ Period: *{period} days*\n"
                f"📄 Reason: *{reason}*"
            )
        else:
            msg = "⚠️ Unable to check UID. Try again later."

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ API Error. Please try again later.")

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_uid))

    print("🤖 Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
