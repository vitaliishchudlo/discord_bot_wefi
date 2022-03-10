import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cur = self.conn.cursor()


db_conn = Database()
