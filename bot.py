import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")


client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Gemini Telegram Bot Started!\n\nSend me any message."
    )


async def ask_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )

        answer = response.text

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"Error: {str(e)}"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ask_gemini
        )
    )

    app.add_error_handler(error_handler)

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()