import app_mode


TG_TOKEN = '123'
DB_HOST = 'mocoronco.mysql.pythonanywhere-services.com'
DB_USER = 'mocoronco'
DB_PASSWORD = '77777778py'
DB_NAME = 'mocoronco$bot'
ADMIN_CHAT_ID = '353684540'

PRODACTION_TG_TOKEN = '321'
PRODACTION_DB_NAME = 'mocoronco$prodaction_bot'

if app_mode.is_prodaction(__file__):
    TG_TOKEN = PRODACTION_TG_TOKEN
    DB_NAME = PRODACTION_DB_NAME