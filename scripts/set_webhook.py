import requests
from prodaction.config import TG_TOKEN as PRODACTION_TG_TOKEN
from test.config import TG_TOKEN as TEST_TG_TOKEN


set_test_bot_webhook = 'https://api.telegram.org/bot{}/setWebhook?url=https://mocoronco.pythonanywhere.com/{}'.format(TEST_TG_TOKEN, TEST_TG_TOKEN)
requests.get(set_test_bot_webhook)
print('set test bot web hook')

set_prodaction_bot_webhook = 'https://api.telegram.org/bot{}/setWebhook?url=https://mocoronco.pythonanywhere.com/{}'.format(PRODACTION_TG_TOKEN, PRODACTION_TG_TOKEN)
requests.get(set_prodaction_bot_webhook)
print('set prodaction bot web hook')