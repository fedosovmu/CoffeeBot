from telegram import Bot
from telegram import Update
import app_mode
if app_mode.is_prodaction(__file__):
    from prodaction.db_handler import DbHandler
    from prodaction.user_model import User
    from prodaction.config import PRODACTION_TG_TOKEN as TG_TOKEN
    from prodaction.config import ADMIN_CHAT_ID
    import prodaction.logger as logger
    import prodaction.bot_messages  as bot_messages
else:
    from test.db_handler import DbHandler
    from test.user_model import User
    from test.config import TG_TOKEN
    from test.config import ADMIN_CHAT_ID
    import test.logger as logger
    import test.bot_messages as bot_messages


class CoffeeBot():
    def __init__(self):
        self.bot = Bot(TG_TOKEN)
        self.db_handler = DbHandler()
        logger.log_text('BOT STARTED')


    def process_update(self, update: Update):
        text = update.effective_message.text
        logger.log_update(update)
        if text != None:
            if text[0] == '/':
                if text == '/start':
                    self.process_start_command(update)
                elif text == '/help':
                    self.process_help_command(update)
                elif text == '/search':
                    self.process_search_command(update)
                elif text == '/stop':
                    self.process_stop_command(update)
                elif text == '/contact':
                    self.process_contact_command(update)
                elif text == '/admin_info':
                    self.process_admin_info_command(update)
                else:
                    self.process_unknown_command(update)
            else:
                self.process_message(update)
        else:
            self.process_data_message(update)


    def process_start_command(self, update):
        reply_text = bot_messages.start_message
        update.message.reply_text(reply_text)


    def process_help_command(self, update):
        reply_text ='/help - Показать список команд\n' \
                    '/search - Начать поиск собеседника\n' \
                    '/stop - Остановить поиск собеседника, закончить разговор\n' \
                    '/contact - Предложить собеседнику обмен контактами'
        update.message.reply_text(reply_text)


    def process_search_command(self, update):
        user = User.create_from_update(update)
        user_status = user.get_status()
        if user_status == "default":
            searching_users_ids = self.db_handler.select_searching_users_ids()
            if len(searching_users_ids) > 0:
                for searching_user_id in searching_users_ids:
                    if user.user_id != searching_user_id:
                        companion = User.create_from_db_searching_table(searching_user_id)
                        companion.stop_search()
                        user.start_dialogue(companion)
                        reply_text = 'Собеседник найден. Для выхода из чата введите команду /stop'
                        self.bot.send_message(companion.user_id, reply_text)
                        break
            else:
                reply_text = 'Начинаю поиск... Для остановки поиска введите команду /stop'
                user.start_search()
        elif user_status == "searching":
            reply_text = 'Поиск уже идёт. Для остановки поиска введите команду /stop'
        elif user_status == "chatting":
            reply_text = 'Вы находитесь в чате с другим пользователем. Для выхода из чата введите команду /stop'
        update.message.reply_text(reply_text)


    def process_stop_command(self, update):
        user = User.create_from_update(update)
        user_status = user.get_status()
        if user_status == 'default':
            reply_text = 'Поиск уже остановлен. Для начала нового поиска введите команду /search'
        elif user_status == 'searching':
            reply_text = 'Поиск остановлен. Для начала нового поиска введите команду /search'
            user.stop_search()
        elif user_status == 'chatting':
            companion = user.get_companion()
            user.stop_dialogue()
            companion_reply_text = 'Ваш собеседник покинул чат. Для начала нового поиска введите команду /search'
            self.bot.send_message(companion.user_id, companion_reply_text)
            reply_text = 'Вы вышли из чата. Для начала нового поиска введите команду /search'
        update.message.reply_text(reply_text)


    def process_contact_command(self, update):
        reply_text = '*Данная команда еще не реализована*'
        update.message.reply_text(reply_text)


    def process_unknown_command(self, update):
        reply_text = 'Неизвестная команда. Для просмотра доступных команд введите /help'
        update.message.reply_text(reply_text)


    def process_message(self, update):
        user = User.create_from_update(update)
        companion = user.get_companion()
        if companion != None:
            text = update.effective_message.text
            companion_reply_text = 'Собеседник: ' + text
            self.bot.send_message(companion.user_id, companion_reply_text)
        else:
            user_status = user.get_status()
            if user_status == 'default':
                reply_text = 'Для просмотра доступных команд введите /help'
            elif user_status == 'searching':
                reply_text = 'В данный момент мы ищим вам собеседника. Для прекращения поиска введите /stop. Для просмотра доступных команд введите /help'
            update.message.reply_text(reply_text)


    def process_data_message(self, update):
        user = User.create_from_update(update)
        companion = user.get_companion()
        if companion != None:
            photo = update.effective_message.photo
            if photo != None:
                self.bot.send_photo(companion.user_id, photo)
            else:
                companion_reply_text = 'Типичный дизайнер: ' + str(update.effective_message)
                self.bot.send_message(companion.user_id, companion_reply_text)
        else:
            reply_text = 'Для просмотра доступных команд введите /help'
            update.message.reply_text(reply_text)


    def process_admin_info_command(self, update):
        user = User.create_from_update(update)
        if user.user_id == ADMIN_CHAT_ID:
            reply_text = 'admin info:'
            reply_text += '\napp mode: ' + app_mode.get_app_mode(__file__).upper()
            reply_text += '\nsearching users: ' + str(self.db_handler.select_searching_users_ids())
            reply_text += '\nchatting users: ' + str(self.db_handler.select_chatting_users_ids())
            reply_text += '\n' + str(update.effective_message)
            reply_text += ''
            reply_text += ''
            reply_text += '\n/help /admin_info'
            self.send_message_to_admin(reply_text)
        else:
            self.process_unknown_command(update)


    def send_message_to_admin(self, text):
        logger.log_text('send message to admin')
        self.bot.send_message(ADMIN_CHAT_ID, text)


