import pymysql
from pymysql.cursors import DictCursor
import config

class DbHandler():
    def __init__(self):
        pass


    def connect(self):
        self.connection = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            db=config.DB_NAME,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        self.cursor = self.connection.cursor()
        print('create connection')


    def close_connection(self):
        self.connection.close()
        print('close connection')


    def select_searching_users_ids(self):
        self.connect()
        try:
            query = """
                SELECT
                    user_id, chat_id
                FROM
                    searching_user
                """
            self.cursor.execute(query)
            result = []
            for row in self.cursor:
                result.append(row["user_id"])
            return result
        finally:
            self.close_connection()


    def select_searching_user(self, user_id):
        self.connect()
        try:
            query = """
                SELECT
                    user_id, chat_id
                FROM
                    searching_user
                WHERE
                    user_id = %s
                """
            self.cursor.execute(query, user_id)
            for row in self.cursor:
                return row
        finally:
            self.close_connection()


    def insert_searching_user(self, user_id, chat_id):
        self.connect()
        try:
            query = """
                INSERT INTO searching_user
                	(user_id, chat_id)
                SELECT %s, %s
                FROM DUAL
                WHERE NOT EXISTS (SELECT 1 FROM searching_user WHERE user_id = %s)
            """
            self.cursor.execute(query, (user_id, chat_id, user_id))
            self.connection.commit()
        finally:
            self.close_connection()


    def delete_searching_user(self, user_id):
        self.connect()
        try:
            query = """
                DELETE FROM searching_user
                WHERE user_id = %s
            """
            self.cursor.execute(query, user_id)
            self.connection.commit()
        finally:
            self.close_connection()


    def select_chatting_users_ids(self):
        self.connect()
        try:
            query = """
                SELECT
                    user_id, chat_id, companion_user_id, companion_chat_id
                FROM
                    chatting_user
                """
            self.cursor.execute(query)
            result = []
            for row in self.cursor:
                result.append(row["user_id"])
            return result
        finally:
            self.close_connection()


    def select_chatting_user(self, user_id):
        self.connect()
        try:
            query = """
                SELECT
                    user_id, chat_id, companion_user_id, companion_chat_id
                FROM
                    chatting_user
                WHERE
                    user_id = %s
                """
            self.cursor.execute(query, user_id)
            for row in self.cursor:
                return row
        finally:
            self.close_connection()


    def insert_chatting_users(self, user_id, chat_id, companion_user_id, companion_chat_id):
        self.connect()
        try:
            query = """
                INSERT INTO chatting_user
                	(user_id, chat_id, companion_user_id, companion_chat_id)
                SELECT %s, %s, %s, %s
                FROM DUAL
                WHERE NOT EXISTS (SELECT 1 FROM chatting_user WHERE user_id = %s OR companion_user_id = %s)
            """
            self.cursor.execute(query, (user_id, chat_id, companion_user_id, companion_chat_id, user_id, user_id))
            self.cursor.execute(query, (companion_user_id, companion_chat_id, user_id, chat_id, companion_user_id, companion_user_id))
            self.connection.commit()
        finally:
            self.close_connection()


    def delete_chatting_users(self, user_id):
        self.connect()
        try:
            query = """
                DELETE FROM chatting_user
                WHERE user_id = %s OR companion_user_id = %s
            """
            self.cursor.execute(query, (user_id, user_id))
            self.connection.commit()
        finally:
            self.close_connection()



if __name__ == '__main__':
    # test db handler
    db_handler = DbHandler()
    #db_handler.insert_searching_user('001','002')
    #users = db_handler.select_searching_users_ids()
    #user_info = db_handler.select_searching_user(users[0])



    #db_handler.insert_chatting_users('123', '123', '321', '321')
    #db_handler.delete_chatting_users('123')
    #users = db_handler.select_chatting_users_ids()
    #print(users)
    #user_info = db_handler.select_chatting_user(users[0])
    #print(user_info)















