from telegram import Bot
from telegram import Update
#from telegram.ext import Dispatcher
#from telegram.ext import MessageHandler
#from telegram.ext import CommandHandler
#from telegram.ext import Filters
from db_handler import DbHandler
from user_model import User
from config import TG_TOKEN


class CoffeeBot():
    def __init__(self):
        self.bot = Bot(TG_TOKEN)
        self.db_handler = DbHandler()
        #dispatcher = Dispatcher(bot, None, workers=0)
        #dispatcher.add_handler(CommandHandler("help", help_command_handler))


    def process_update(self, update: Update):
        #bot.bot.dispatcher.process_update(update)
        text = update.effective_message.text
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
            else:
                self.process_unknown_command(update)
        else:
            self.process_unknown_command(update)


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
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        user = User(user_id, chat_id)
        user_status = user.get_status()
        if user_status == "default":
            reply_text = 'Начинаю поиск'
            user.start_search()
        elif user_status == "searching":
            reply_text = 'Поиск уже идёт. Для остановки поиска введите команду /stop'
        elif user_status == "chatting":
            reply_text = 'Вы находитесь в чате с другим пользователем. Для выхода из чата введите команду /stop'

        reply_text += ' ' + str(self.db_handler.select_searching_user())
        update.message.reply_text(reply_text)


    def process_stop_command(self, update):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        user = User(user_id, chat_id)
        user_status = user.get_status()
        if user_status == "default":
            reply_text = 'Поиск уже остановлен. Для начала нового поиска введите команду /search'
        elif user_status == "searching":
            reply_text = 'Останавливаю поиск'
            user.stop_search()
        elif user_status == "chatting":
            reply_text = 'Выхожу из чата *не реализованно*'

        reply_text += ' ' + str(self.db_handler.select_searching_user())
        update.message.reply_text(reply_text)


    def process_contact_command(self, update):
        reply_text = '*Данная команда еще не реализована*'
        update.message.reply_text(reply_text)


    def process_unknown_command(self, update):
        reply_text = 'Неизвестная команда. Для просмотра доступных команд введите /help'
        update.message.reply_text(reply_text)


    def send_message_to_admin(self, text):
        admin_chat_id = '353684540'
        self.bot.send_message(admin_chat_id, text)

    #def process_echo_command(self, update):
    #    #chat_id = update.effective_message.chat_id
    #    user = update.effective_user
    #    name = user.first_name if user else 'аноним'
    #    text = update.effective_message.text
    #    reply_text = f'Привет, {name}!\n\"{text}\"'
    #    update.message.reply_text(reply_text)
    #    #self.bot.send_message(chat_id, reply_text)


