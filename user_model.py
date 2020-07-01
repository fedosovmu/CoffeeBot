from db_handler import DbHandler


class User:
    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = str(chat_id)
        self.db_handler = DbHandler()


    def get_status(self):
        users = self.db_handler.select_searching_user()
        if self.user_id in users:
            return "searching"
        else:
            return "default"
        return "chatting"


    def start_search(self):
        self.db_handler.insert_searching_user(self.user_id, self.chat_id)


    def stop_search(self):
        self.db_handler.delete_searching_user(self.user_id)


    def get_companion(self):
        pass


    def start_dialogue(self):
        pass


    def stop_dialogue(self):
        pass
