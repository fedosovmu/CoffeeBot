from flask import Flask, request
from telegram import Update
from bot import CoffeeBot


bot = CoffeeBot()
app = Flask(__name__)


@app.route('/')
def main_page():
    return 'this is telegram bot webhook site'


@app.route('/'+bot.TG_TOKEN, methods=["GET", "POST"])
def telegram_bot_webhook_receive_update():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), bot.bot)
        bot.process_update(update)
    return '{"ok": True}'