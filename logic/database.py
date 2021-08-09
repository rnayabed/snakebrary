import sqlite3

from pathlib import Path
from logic.user import User, UserSettings


class Database:
    __db_con: sqlite3.dbapi2

    @staticmethod
    def get_database_location():
        return str(Path.home()) + "/snakebrary.db"

    @staticmethod
    def create_connection():
        global __db_con
        __db_con = sqlite3.connect(Database.get_database_location())

    @staticmethod
    def close_connection():
        global __db_con
        __db_con.close()

    @staticmethod
    def create_new_tables():
        Database.create_new_users_table()
        Database.create_new_account_settings_table()

    @staticmethod
    def create_new_users_table():
        global __db_con
        __db_con.execute('''CREATE TABLE users
        (username   TEXT  PRIMARY KEY  NOT NULL,
        password    TEXT    NOT NULL,
        password_hint   TEXT    NOT NULL,
        name    TEXT    NOT NULL,
        privilege   INT NOT NULL,
        date_time_created    TEXT    NOT_NULL);''')

    @staticmethod
    def create_new_account_settings_table():
        global __db_con
        __db_con.execute('''CREATE TABLE account_settings
        (username   TEXT  PRIMARY KEY  NOT NULL,
        theme    TEXT    NOT NULL,
        accent_colour   TEXT    NOT NULL);''')

    @staticmethod
    def create_new_user(new_user: User):
        global __db_con
        __db_con.execute(f'''INSERT INTO users(username, password, password_hint, name, privilege, date_time_created)
        VALUES ("{new_user.username}", "{new_user.password}", 
        "{new_user.password_hint}", "{new_user.name}", "{new_user.privilege}",
        "{new_user.date_time_created}");''')

        __db_con.execute(f'''INSERT INTO account_settings(username, theme, accent_colour)
        VALUES ("{new_user.username}", "light", "purple")''')

        __db_con.commit()

    @staticmethod
    def get_users_by_username(username):
        return Database.__filter_users(f'SELECT * FROM users WHERE username="{username}"')

    @staticmethod
    def get_all_users():
        return Database.__filter_users(f'SELECT * FROM users')

    @staticmethod
    def __filter_users(sql):
        global __db_con
        __db_con.execute(sql)
        users = list(__db_con.execute(sql))

        tbr = []

        for i in users:
            tba = User(i[0], i[1], i[2], i[3], i[4], i[5])
            tba.print_details()
            tbr.append(tba)

        return tbr


    @staticmethod
    def get_user_settings(username):
        global __db_con
        s = list(__db_con.execute(f'SELECT * FROM account_settings WHERE username="{username}"'))[0]
        return UserSettings(s[0], s[1], s[2])

    @staticmethod
    def set_user_settings(user_settings: UserSettings):
        global __db_con
        __db_con.execute(f'UPDATE account_settings '
                             f'SET theme="{user_settings.theme}", accent_colour="{user_settings.accent_colour}" '
                             f'WHERE username="{user_settings.username}" ')

        Database.save_database()

    @staticmethod
    def save_database():
        global __db_con
        __db_con.commit()

    @staticmethod
    def print_all_users():
        global __db_con
        print(list(__db_con.execute("SELECT * FROM users")))

    @staticmethod
    def is_new_setup():
        global __db_con
        return len(list(__db_con.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users";'))) == 0

    @staticmethod
    def delete_user(username):
        global __db_con
        __db_con.execute(f'DELETE FROM users WHERE username="{username}"')
        __db_con.execute(f'DELETE FROM account_settings WHERE username="{username}"')  

        Database.save_database()