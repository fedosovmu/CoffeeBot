from telegram import Bot
from telegram import Update
from prodaction.db_handler import DbHandler
from prodaction.user_model import User
from prodaction.config import IS_PRODACTION
from prodaction.config import TG_TOKEN
from prodaction.config import ADMIN_CHAT_ID


class CoffeeBot():
    def __init__(self):
        self.bot = Bot(TG_TOKEN)
        self.db_handler = DbHandler()


    def process_update(self, update: Update):
        text = update.effective_message.text
        self.log_update(update)
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


    def process_start_command(self, update):
        reply_text = 'Привет, {}. Добро пожаловать в дизайн-кафе. ' \
                     'Надеюсь ты хорошо проведешь время общаясь с другими посетителями. ' \
                     'Для того чтобы начать поиск собеседника введи команду /search, ' \
                     'для просмотра списка доступных команд введи команду /help' \
                     ''.format(update.effective_user.first_name)
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
            companion_reply_text = 'Типичный дизайнер: ' + update.effective_message.text
            self.bot.send_message(companion.user_id, companion_reply_text)
        else:
            user_status = user.get_status()
            if user_status == 'default':
                reply_text = 'Для просмотра доступных команд введите /help'
            elif user_status == 'searching':
                reply_text = 'В данный момент мы ищим вам собеседника. Для прекращения поиска введите /stop. Для просмотра доступных команд введите /help'
            update.message.reply_text(reply_text)


    def process_admin_info_command(self, update):
        user = User.create_from_update(update)
        if user.user_id == ADMIN_CHAT_ID:
            if IS_PRODACTION:
                prodaction_str = 'PRODACTION'
            else:
                prodaction_str = 'TEST'
            reply_text = 'admin info: ' + prodaction_str + ' ' + str(self.db_handler.select_searching_users_ids()) + ' ' + str(self.db_handler.select_chatting_users_ids())
            self.send_message_to_admin(reply_text)
        else:
            self.process_unknown_command(update)


    def log_update(self, update):
        name = update.effective_user.first_name + ' ' + update.effective_user.last_name
        user_id = update.effective_user.id
        text = update.effective_message.text
        log_message = 'PROCESS MESSAGE ("{}":"{}":"{}")'.format(name, user_id, text)
        print(log_message)


    def send_message_to_admin(self, text):
        self.bot.send_message(ADMIN_CHAT_ID, text)


