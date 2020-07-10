import app_mode


TG_TOKEN = '1374409729:AAGfeRsaweSWtDf91ZnSDLYN1PynbsfYHzY'
DB_HOST = 'mocoronco.mysql.pythonanywhere-services.com'
DB_USER = 'mocoronco'
DB_PASSWORD = '77777778py'
DB_NAME = 'mocoronco$bot'
ADMIN_CHAT_ID = '353684540'

PRODACTION_TG_TOKEN = '1101055853:AAGU7qr9MTpD0OCDr-QLf73pzGQvTfe2sQQ'
PRODACTION_DB_NAME = 'mocoronco$prodaction_bot'

if app_mode.is_prodaction(__file__):
    TG_TOKEN = PRODACTION_TG_TOKEN
    DB_NAME = PRODACTION_DB_NAME