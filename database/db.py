import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cur = self.conn.cursor()
        if self.conn:
            print('Database connection...OK')
        else:
            print('Database connection...ERROR')

    def refresh_achivement_users(self):
        pass

    def reset_sequecne(self, table_name):
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
            self.cur.execute('DELETE FROM achivement_users')
            sql = 'INSERT INTO achivement_users(discord_id, name) VALUES (?, ?)'
            for user in users:
                val = (user.id, user.name)
                self.cur.execute(sql, val)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as err:
            print(err)
            return False
