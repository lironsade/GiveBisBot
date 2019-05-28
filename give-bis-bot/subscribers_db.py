import sqlite3


class SubscribersDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('subscribers.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurants
                               (chat_id TEXT UNIQUE, rest_name TEXT, food TEXT, 
                               tel TEXT, location TEXT, rest_id INTEGER PRIMARY KEY(rest_id))''')

    def insert(self, chat_id, rest_name, food, tel, location, rest_id):
        self.cursor.execute('''INSERT INTO Restaurants VALUES ({})'''.format(chat_id, rest_name, food, tel, location, rest_id))
        self.conn.commit()

    def delete(self, rest_id):
        self.cursor.execute('''DELETE FROM subscribers WHERE id={}'''.format(rest_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_all_restaurants(self):
        return [rest_id for (rest_id, ) in self.cursor.execute('SELECT rest_id FROM Restaurants')]
