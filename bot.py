import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# Render Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Bot Running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 *Welcome to Dhavalgiri Bot!* 🤖\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🇬🇧 *Hello!*\n"
        "I'm *Dhavalgiri Bot*, your smart AI assistant.\n"
        "I'm here to help you with coding, studies, writing, ideas, problem-solving, technology, and much more.\n\n"
        "🇮🇳 *नमस्ते!*\n"
        "मैं *Dhavalgiri Bot* हूँ।\n"
        "कोडिंग, पढ़ाई, लेखन, नए आइडियाज़, टेक्नोलॉजी, सामान्य जानकारी या किसी भी सवाल में आपकी मदद करने के लिए हमेशा तैयार हूँ।\n\n"
        "💬 *Just send your message*\n"
        "📩 *बस अपना संदेश भेजिए*\n\n"
        "✨ Ask anything, anytime.\n"
        "🚀 *Let's begin our journey together!*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💙 Powered by *Dhaval goswami*\n"
        "⚡ Fast • Smart • Reliable"
    )

    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("🤖 Bot Started...")
    application.run_polling()


if __name__ == "__main__":
    main()