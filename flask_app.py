from flask import Flask, request
from telegram import Update
from coffee_bot import CoffeeBot as TestCoffeeBot
from config import TG_TOKEN as TEST_TG_TOKEN
from prodaction.coffee_bot import CoffeeBot as ProdactionCoffeeBot
from prodaction.config import TG_TOKEN as PRODACTION_TG_TOKEN


prodaction_bot = ProdactionCoffeeBot()
test_bot = TestCoffeeBot()
app = Flask(__name__)


@app.route('/')
def main_page():
    return 'this is telegram bot webhook site'


@app.route('/'+PRODACTION_TG_TOKEN, methods=["GET", "POST"])
def prodaction_bot_webhook_receive_update():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), prodaction_bot.bot)
        prodaction_bot.process_update(update)
    return '{"ok": True}'


@app.route('/'+'1374409729:AAGfeRsaweSWtDf91ZnSDLYN1PynbsfYHzY', methods=["GET", "POST"])
def test_bot_webhook_receive_update():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), test_bot.bot)
        test_bot.process_update(update)
    return '{"ok": True}'