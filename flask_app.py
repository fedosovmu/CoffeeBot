from flask import Flask, request
from telegram import Update
try:
    from coffee_bot import CoffeeBot as TestCoffeeBot
    from config import TG_TOKEN as TEST_TG_TOKEN
except:
    print('TEST BOT EXEPTION: import coffe_bot, config')
from prodaction.coffee_bot import CoffeeBot as ProdactionCoffeeBot
from prodaction.config import TG_TOKEN as PRODACTION_TG_TOKEN


prodaction_bot = ProdactionCoffeeBot()
try:
    test_bot = TestCoffeeBot()
except:
    print('TEST BOT EXEPTION: create TestCoffeeBot')
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

try:
    @app.route('/'+TEST_TG_TOKEN, methods=["GET", "POST"])
    def test_bot_webhook_receive_update():
        if request.method == "POST":
            update = Update.de_json(request.get_json(), test_bot.bot)
            test_bot.process_update(update)
        return '{"ok": True}'
except:
    print('TEST BOT EXEPTION: test_bot_webhook_receive_update')