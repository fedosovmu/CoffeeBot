from telegram import Update
import app_mode


bot_type = '{}-BOT'.format(app_mode.get_app_mode(__file__).upper())


def log_update(update: Update):
    name = update.effective_user.first_name + ' ' + update.effective_user.last_name
    user_id = update.effective_user.id
    text = update.effective_message.text
    if text != None:
        log_message = '======= {} «LOG UPDATE» ("{}":"{}") "{}"'.format(bot_type, name, user_id, text)
    else:
        log_message = '======= {} «LOG UPDATE» ("{}":"{}") (text == None) update_id: {}'.format(bot_type, name, user_id, str(update['update_id']))
    print(log_message)


def log_text(text, text_detail = ''):
    log_message = '======= {} «{}» {}'.format(bot_type, text, text_detail)
    print(log_message)