import os
import logging
from threading import Thread
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- TOKEN ----------------
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ---------------- MESSAGES ----------------
INVITE_MESSAGE = """Invite Code: <code>5MJ3P</code>
🔗 Link: http://ptier.xyz/register?i=5MJ3P
"""

CONTACT_MESSAGE = "Contact to buy:\nhttps://t.me/Don_marlon333"

# ---------------- KEYBOARD ----------------
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Invite Code")
    markup.row("Contact to buy")
    return markup


# ---------------- COMMANDS ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        INVITE_MESSAGE,
        reply_markup=main_keyboard()
    )


@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    text = message.text

    if text == "Invite Code":
        bot.send_message(message.chat.id, INVITE_MESSAGE)

    elif text == "Contact to buy":
        bot.send_message(message.chat.id, CONTACT_MESSAGE)


# ---------------- FLASK WEB SERVER ----------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is alive ✅"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# ---------------- RUN BOT ----------------
def run_bot():
    logging.info("Bot polling started...")
    bot.infinity_polling(skip_pending=True)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    Thread(target=run_bot).start()

    run_web()


