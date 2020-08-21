from flask import Flask, request
from telegram import Update
from prodaction.coffee_bot import CoffeeBot as ProdactionCoffeeBot
from prodaction.config import TG_TOKEN as PRODACTION_TG_TOKEN
import traceback


prodaction_bot = ProdactionCoffeeBot()
app = Flask(__name__)


@app.route('/')
def main_page():
    return 'this is telegram bot webhook site'


# PRODACTION BOT
@app.route('/'+PRODACTION_TG_TOKEN, methods=["GET", "POST"])
def prodaction_bot_webhook_receive_update():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), prodaction_bot.bot)
        prodaction_bot.process_update(update)
    return '{"ok": True}'


# TEST BOT
try:
    from test.coffee_bot import CoffeeBot as TestCoffeeBot
    from test.config import TG_TOKEN as TEST_TG_TOKEN

    test_bot = TestCoffeeBot()

    @app.route('/'+TEST_TG_TOKEN, methods=["GET", "POST"])
    def test_bot_webhook_receive_update():
        if request.method == "POST":
            update = Update.de_json(request.get_json(), test_bot.bot)
            test_bot.process_update(update)
        return '{"ok": True}'

except:
    print('======= TEST-BOT «EXEPTION!»')
    error_message = traceback.format_exc().split('\n')
    for line in error_message:
        print('======= ' + str(line))