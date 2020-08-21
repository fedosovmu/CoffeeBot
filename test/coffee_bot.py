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
        logger.log_text('BOT STARTED', '=======')
        self.debug_mode = False
        self.echo_mode = False


    def process_update(self, update: Update):
        logger.log_update(update)
        text = update.effective_message.text
        user = User.create_from_update(update)
        is_admin = user.user_id == ADMIN_CHAT_ID
        if self.debug_mode and is_admin:
            update.message.reply_text(str(update) + '\n/debug_off')

        if text != None:
            if text[0] == '/':
                if text == '/start':
                    self.process_start_command(update)
                elif text == '/help':
                    self.process_help_command(update, is_admin)
                elif text == '/search':
                    self.process_search_command(update)
                elif text == '/stop':
                    self.process_stop_command(update)
                elif text == '/contact':
                    self.process_contact_command(update)
                elif is_admin:
                    if text == '/admin_info':
                        self.process_admin_info_command(update)
                    elif text == '/test_button':
                        self.process_test_button_command(update)
                    elif text == '/debug_on':
                        self.process_debug_on_command(update)
                    elif text == '/debug_off':
                        self.process_debug_off_command(update)
                    elif text == '/echo_on':
                        self.process_echo_on_command(update)
                    elif text == '/echo_off':
                        self.process_echo_off_command(update)
                    else:
                        self.process_unknown_command(update)
                else:
                    self.process_unknown_command(update)
            else:
                self.process_message(update, is_admin)
        else:
            self.process_data_message(update, is_admin)


    def process_start_command(self, update):
        #markup = types.InlineKeyboardMarkup(row_width=2)
        #item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
        #item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
        #markup.add(item1, item2)
        reply_text = bot_messages.start_message
        update.message.reply_text(reply_text)


    def process_help_command(self, update, is_admin):
        reply_text ='/help - Показать список команд\n' \
                    '/search - Начать поиск собеседника\n' \
                    '/stop - Остановить поиск собеседника, закончить разговор\n' \
                    '/contact - Предложить собеседнику обмен контактами'
        if is_admin:
            reply_text += '\n====== ADMIN ONLY ======' \
                          '\n/admin_info' \
                          '\n/test_button' \
                          '\n/debug_on' \
                          '\n/debug_off' \
                          '\n/echo_on' \
                          '\n/echo_off'
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


    def process_message(self, update, is_admin):
        logger.log_text('PROCCESS MESSAGE')
        user = User.create_from_update(update)
        companion = user.get_companion()
        if companion == None and self.echo_mode and is_admin:
            companion = user.create_from_id(ADMIN_CHAT_ID)
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


    def process_data_message(self, update, is_admin):
        logger.log_text('PROCESS DATA MESSAGE')
        user = User.create_from_update(update)
        companion = user.get_companion()
        if companion == None and self.echo_mode and is_admin:
            companion = user.create_from_id(ADMIN_CHAT_ID)
        if companion != None:
        #    photo = update.effective_message.photo
        #    if photo != None:
            logger.log_text('PROCESS DATA MESSAGE', 'send photo')
            companion_reply_text = 'Собеседник: ' + '[Данные]'
            self.bot.send_message(companion.user_id, companion_reply_text)
        #    else:
        #        logger.log_text('PROCESS DATA MESSAGE', 'cannot find photo')
        else:
            reply_text = 'Для просмотра доступных команд введите /help'
            update.message.reply_text(reply_text)
        logger.log_text('PROCESS DATA MESSAGE', 'end process')


    def process_admin_info_command(self, update):
        logger.log_text('PROCESS ADMIN INFO')
        reply_text = 'admin info:'
        reply_text += '\napp mode: ' + app_mode.get_app_mode(__file__).upper()
        reply_text += '\ndebug mode: ' + str(self.debug_mode)
        reply_text += '\necho mode: ' + str(self.echo_mode)
        reply_text += '\nsearching users: ' + str(self.db_handler.select_searching_users_ids())
        reply_text += '\nchatting users: ' + str(self.db_handler.select_chatting_users_ids())
        #reply_text += '\n' + str(update.effective_message)
        reply_text += ''
        reply_text += ''
        reply_text += '\n/help /admin_info'
        #update.message.reply_text(reply_text)
        self.send_message_to_admin(reply_text)
        logger.log_text('PROCESS ADMIN INFO', 'end process')



    def process_test_button_command(self, update):
        reply_text = '[КНОПКА]'
        update.message.reply_text(reply_text)

        #markup = types.InlineKeyboardMarkup(row_width=2)
        #item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
        #item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
        #markup.add(item1, item2)


    def process_debug_on_command(self, update):
        reply_text = '[Режим дебага включен] /debug_off'
        self.debug_mode = True
        update.message.reply_text(reply_text)


    def process_debug_off_command(self, update):
        reply_text = '[Режим дебага выключен]'
        self.debug_mode = False
        update.message.reply_text(reply_text)


    def process_echo_on_command(self, update):
        reply_text = '[Режим эхо включен] /echo_off'
        self.echo_mode = True
        update.message.reply_text(reply_text)


    def process_echo_off_command(self, update):
        reply_text = '[Режим эхо выключен]'
        self.echo_mode = False
        update.message.reply_text(reply_text)


    def send_message_to_admin(self, text):
        logger.log_text('send message to admin')
        self.bot.send_message(ADMIN_CHAT_ID, text)


