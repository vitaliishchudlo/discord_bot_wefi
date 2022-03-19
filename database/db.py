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

    def get_captcha_text(self, discord_id):
        sql = 'SELECT captcha FROM registration_users WHERE discord_id=?'
        val = (discord_id,)
        self.cur.execute(sql, val)
        return self.cur.fetchone()[0]

    def get_achievement_users(self):
        sql = 'SELECT username FROM achievement_users'
        self.cur.execute(sql)
        response = self.cur.fetchall()
        if not response:
            return False
        return [x[0] for x in response]

    def get_achievement_games(self):
        sql = 'SELECT * FROM achievement_games'
        self.cur.execute(sql)
        response = self.cur.fetchall()
        if not response:
            return False
        return response

    def get_achievements_data(self, discord_id, discord_name, game, type, count):
        sql_select = 'SELECT count FROM achievement_statistics ' \
                     'WHERE discord_id=?' \
                     'AND game=?' \
                     'AND type=?'
        val_select = (discord_id, game, type)
        self.cur.execute(sql_select, val_select)
        response = self.cur.fetchall()
        if response:
            count += response[0][0]
            sql_update = 'UPDATE achievement_statistics ' \
                         'SET count=? ' \
                         'WHERE discord_id=?' \
                         'AND game=?' \
                         'AND type=?'
            val_update = (count, discord_id, game, type,)
            self.cur.execute(sql_update, val_update)
            self.conn.commit()
            return count
        sql_insert = 'INSERT INTO achievement_statistics(discord_id, username,game, type, count)' \
                     'VALUES(?,?,?,?,?)'
        val_insert = (discord_id, discord_name, game, type, count)
        self.cur.execute(sql_insert, val_insert)
        self.conn.commit()
        return count
