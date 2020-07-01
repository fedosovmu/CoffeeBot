from db_handler import DbHandler
from telegram import Update


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
        return User(user["companion_user_id", "companion_chat_id"])


    def start_search(self):
        self.db_handler.insert_searching_user(self.user_id, self.chat_id)


    def stop_search(self):
        self.db_handler.delete_searching_user(self.user_id)


    def start_dialogue(self, companion):
        self.db_handler.insert_chatting_users(self.user_id, self.chat_id, companion.user_id, companion.chat_id)


    def stop_dialogue(self):
        self.db_handler.delete_chatting_users(self.user_id)


if __name__ == '__main__':
    # test user model
    #admin = User('353684540', '353684540')
    #admin = User.create_from_db_searching_table('353684540')
    #user_1 = User('111', '110')
    #user_2 = User('222', '220')
    #user_1.start_dialogue(user_2)

    #print(admin.user_id + ' ' + admin.chat_id)
    pass





