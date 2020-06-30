import pymysql
from pymysql.cursors import DictCursor


class DbHandler():
    def __init__(self):
        pass


    def connect(self):
        self.connection = pymysql.connect(
            host='mocoronco.mysql.pythonanywhere-services.com',
            user='mocoronco',
            password='77777778py',
            db='mocoronco$bot',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        self.cursor = self.connection.cursor()
        print('create connection')


    def close_connection(self):
        self.connection.close()
        print('close connection')


    def select_searching_user(self):
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


    def start_dialogue(user_one_id, user_two_id):
        pass

    def finish_dialogue(self, user_id):
        pass

    def insert_dialogue(self, user_one_id, user_two_id, chat_two_id):
        pass



if __name__ == '__main__':
    # test db handler
    db_handler = DbHandler()
    #db_handler.insert_searching_user('001','002')
    users = db_handler.select_searching_user()
    print(users)




