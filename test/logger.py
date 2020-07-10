from telegram import Update
import app_mode


bot_type = '{}-BOT'.format(app_mode.get_app_mode(__file__).upper())


def log_update(update: Update):
    name = update.effective_user.first_name + ' ' + update.effective_user.last_name
    user_id = update.effective_user.id
    text = update.effective_message.text
    if text != None:
        log_message = '======= {} «PROCESS MESSAGE» ("{}":"{}":"{}")'.format(bot_type, name, user_id, text)
    else:
        log_message = '======= {} «PROCESS MESSAGE» ("{}":"{}":"{}")'.format(bot_type, name, user_id, str(update))
    print(log_message)


def log_text(text):
    log_message = '======= {} «{}»'.format(bot_type, text)
    print(log_message)