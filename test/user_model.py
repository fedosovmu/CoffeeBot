from telegram import Update
import app_mode
if app_mode.is_prodaction(__file__):
    from prodaction.db_handler import DbHandler
else:
    from test.db_handler import DbHandler


class User:
    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = str(chat_id)
        self.db_handler = DbHandler()


    @staticmethod
    def create_from_update(update: Update):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        return User(user_id, chat_id)


    @staticmethod
    def create_from_db_searching_table(user_id):
        db_handler = DbHandler()
        user = db_handler.select_searching_user(str(user_id))
        return User(user["user_id"], user["chat_id"])


    @staticmethod
    def create_from_id(user_id):
        return User(user_id, user_id)


    def get_status(self):
        searching_users = self.db_handler.select_searching_users_ids()
        chatting_users = self.db_handler.select_chatting_users_ids()
        if self.user_id in searching_users:
            return "searching"
        elif self.user_id in chatting_users:
            return "chatting"
        else:
            return "default"


    def get_companion(self):
        user = self.db_handler.select_chatting_user(self.user_id)
        if user != None:
            return User(user["companion_user_id"], user["companion_chat_id"])
        else:
            return None


    def start_search(self):
        self.db_handler.insert_searching_user(self.user_id, self.chat_id)


    def stop_search(self):
        self.db_handler.delete_searching_user(self.user_id)


    def start_dialogue(self, companion):
        self.db_handler.insert_chatting_users(self.user_id, self.chat_id, companion.user_id, companion.chat_id)


    def stop_dialogue(self):
        self.db_handler.delete_chatting_users(self.user_id)


if __name__ == '__main__':
    pass
    # test user model
    #db_handler = DbHandler()
    #admin = User('353684540', '353684540')
    #admin = User.create_from_db_searching_table('353684540')

    #user_1 = User('111', '110')
    #user_2 = User('222', '220')
    #user_1.start_dialogue(user_2)

    #db_handler.delete_chatting_users('111')

    #chatting_users_ids = db_handler.select_chatting_users_ids()
    #chatting_user = db_handler.select_chatting_user(chatting_users_ids[0])
    #user_1 = User(chatting_user["user_id"], chatting_user["chat_id"])
    #user_1.stop_dialogue()
    #companion = user_1.get_companion()
    #print(user_1.user_id, user_1.chat_id)
    #print(companion.user_id, companion.chat_id)

    #database_tables = str(db_handler.select_searching_users_ids()) + ' ' + str(db_handler.select_chatting_users_ids())
    #print(database_tables)
    #chatting_users_ids = db_handler.select_chatting_users_ids()
    #for chatting_user_id in chatting_users_ids:
    #    chatting_user = db_handler.select_chatting_user(chatting_user_id)
    #    print(chatting_user)

    #user_1 = User('111', '110')
    #companion = user_1.get_companion()
    #print(companion)





