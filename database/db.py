import os.path
import sqlite3

from data import config
from .migrations import make_migrations


class Database:
    def __init__(self):
        if not os.path.isfile(config.PATH_DATABASE):
            print('DataBase does not exists. Running migrations...')
            if make_migrations():
                print('Migrations...OK')
        self.conn = sqlite3.connect(config.PATH_DATABASE)
        self.cur = self.conn.cursor()
        if self.conn:
            print('Database connection...OK')
        else:
            print('Database connection...ERROR')

    def refresh_achivement_users(self):
        pass

    def reset_sequecne(self, table_name):
        sql = 'SELECT 1 FROM sqlite_sequence WHERE name=?'
        val = (table_name,)
        self.cur.execute(sql, val)
        if not bool(self.cur.fetchall()):
            return False
        sql = 'UPDATE sqlite_sequence SET seq=? WHERE name=?'
        val = (0, table_name)
        try:
            self.cur.execute(sql, val)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as err:
            print(err)
            return False

    def save_achivement_users(self, users):
        try:
            self.cur.execute('DELETE FROM achievement_users')
            sql = 'INSERT INTO achievement_users(discord_id, username) VALUES (?, ?)'
            for user in users:
                val = (user.id, user.name)
                self.cur.execute(sql, val)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as err:
            print(err)
            return False

    def register_user(self, discord_id, user_name, captcha_text):
        sql_get_user = 'DELETE FROM registration_users WHERE discord_id=?'
        val = (discord_id,)
        self.cur.execute(sql_get_user, val)

        sql = 'INSERT INTO registration_users (discord_id, username, captcha) ' \
              'VALUES (?,?,?)'
        val = (discord_id, user_name, captcha_text)
        self.cur.execute(sql, val)
        self.conn.commit()
        self.conn.close()
