import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# Render Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Bot Running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Gemini Bot Ready")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        content=msg
    )

    await update.message.reply_text(response.text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    application.run_polling()


if __name__ == "__main__":
    main()