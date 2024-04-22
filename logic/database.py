import sqlite3
from ast import literal_eval
from pathlib import Path

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorBuffered

from logic.book import Book, BookRatings
from logic.user import User, UserSettings


class Database:
    __db_con: MySQLConnection
    __db_con_cursor: MySQLCursorBuffered

    __local_db_con: sqlite3.dbapi2
    __local_db_con_cursor: sqlite3.Cursor

    @staticmethod
    def is_connected():
        try:
            return Database.__db_con_cursor is not None
        except:
            return False

    @staticmethod
    def get_local_database_location():
        return str(Path.home()) + "/snakebrary.db"

    @staticmethod
    def create_connection(host, user, password, port):
        Database.__db_con = mysql.connector.connect(host=host, user=user, password=password, port=int(port))
        Database.__db_con.cursor().execute('create database if not exists snakebrary')
        Database.__db_con.cmd_init_db('snakebrary')
        Database.__db_con_cursor = Database.__db_con.cursor(buffered=True)

    @staticmethod
    def create_local_connection():
        Database.__local_db_con = sqlite3.connect(Database.get_local_database_location())
        Database.__local_db_con_cursor = Database.__local_db_con.cursor()

    @staticmethod
    def close_connection():
        if Database.is_connected():
            Database.__db_con_cursor.close()
            Database.__db_con.close()
            Database.__db_con_cursor = None
            Database.__db_con = None

    @staticmethod
    def close_local_connection():
        Database.__local_db_con_cursor.close()
        Database.__local_db_con.close()

    @staticmethod
    def create_local_database_settings_table():
        Database.__local_db_con_cursor.execute('''CREATE TABLE local_settings
        (key   TEXT  PRIMARY KEY  NOT NULL,
        value    TEXT    NOT NULL)''')

    @staticmethod
    def set_local_setting(key, value):
        Database.__local_db_con_cursor.execute(f'''INSERT OR REPLACE INTO local_settings(key, value)
            VALUES ("{key}", "{value}");''')

    @staticmethod
    def get_local_setting(key):
        try:
            return list(Database.__local_db_con_cursor.execute(f'SELECT * FROM local_settings WHERE key="{key}"'))[0][1]
        except:
            return None

    @staticmethod
    def get_local_database_server_host():
        return Database.get_local_setting('server_host')

    @staticmethod
    def get_local_database_server_user():
        return Database.get_local_setting('server_user')

    @staticmethod
    def get_local_database_server_password():
        return Database.get_local_setting('server_password')

    @staticmethod
    def get_local_database_server_port():
        return Database.get_local_setting('server_port')

    @staticmethod
    def set_local_database_server_host(host):
        Database.set_local_setting('server_host', host)

    @staticmethod
    def set_local_database_server_user(user):
        Database.set_local_setting('server_user', user)

    @staticmethod
    def set_local_database_server_password(password):
        Database.set_local_setting('server_password', password)

    @staticmethod
    def set_local_database_server_port(port):
        Database.set_local_setting('server_port', port)

    @staticmethod
    def create_new_tables():
        Database.create_new_users_table()
        Database.create_new_account_settings_table()
        Database.create_new_books_table()
        Database.create_new_books_ratings_table()

    @staticmethod
    def create_new_users_table():
        Database.__db_con_cursor.execute('''CREATE TABLE users
        (username   VARCHAR(50)  PRIMARY KEY  NOT NULL,
        password    TEXT    NOT NULL,
        password_hint   TEXT    NOT NULL,
        name    TEXT    NOT NULL,
        is_disabled BOOLEAN,
        privilege   INT NOT NULL,
        photo   LONGBLOB,
        date_time_created    TEXT    NOT NULL);''')

    @staticmethod
    def create_new_account_settings_table():
        Database.__db_con_cursor.execute('''CREATE TABLE account_settings
        (username   VARCHAR(50)  PRIMARY KEY  NOT NULL,
        theme    TEXT    NOT NULL,
        accent_colour   TEXT    NOT NULL);''')

    @staticmethod
    def create_new_books_table():
        Database.__db_con_cursor.execute('''CREATE TABLE books
        (ISBN   VARCHAR(50)  PRIMARY KEY  NOT NULL,
        name    TEXT    NOT NULL,
        author   TEXT   NOT NULL,
        holders    TEXT    NOT NULL,
        genres    TEXT    NOT NULL,
        price   FLOAT NOT NULL,
        about   TEXT,
        is_unavailable BOOLEAN,
        photo   LONGBLOB,
        date_time_added    TEXT    NOT NULL);''')

    @staticmethod
    def create_new_books_ratings_table():
        Database.__db_con_cursor.execute('''CREATE TABLE books_ratings
        (ISBN   VARCHAR(50)  PRIMARY KEY  NOT NULL,
        ratings   TEXT    NOT NULL);''')

    @staticmethod
    def create_new_user(new_user: User):
        if new_user.photo is None:
            Database.__db_con_cursor.execute(f'''INSERT INTO users
            (username, password, password_hint, name, is_disabled, privilege, photo, date_time_created)
            VALUES ("{new_user.username}", "{new_user.password}", 
            "{new_user.password_hint}", "{new_user.name}", {new_user.is_disabled}, "{new_user.privilege}", NULL,
            "{new_user.date_time_created}");''')
        else:
            Database.__db_con_cursor.execute(f'''INSERT INTO users
            (username, password, password_hint, name, is_disabled, privilege, photo, date_time_created)
            VALUES ("{new_user.username}", "{new_user.password}", 
            "{new_user.password_hint}", "{new_user.name}", {new_user.is_disabled}, "{new_user.privilege}", %s,
            "{new_user.date_time_created}");''', (new_user.photo,))

        Database.__db_con_cursor.execute(f'''INSERT INTO account_settings(username, theme, accent_colour)
        VALUES ("{new_user.username}", "light", "purple")''')

        Database.save_database()

    @staticmethod
    def update_user(user: User):
        if user.photo is None:
            Database.__db_con_cursor.execute(f'''UPDATE users
            SET password="{user.password}", password_hint="{user.password_hint}", name="{user.name}", 
            is_disabled={user.is_disabled}, privilege="{user.privilege}", photo=NULL
            WHERE username="{user.username}"''')
        else:
            Database.__db_con_cursor.execute(f'''UPDATE users
            SET password="{user.password}", password_hint="{user.password_hint}", name="{user.name}", 
            is_disabled={user.is_disabled}, privilege="{user.privilege}", photo=%s
            WHERE username="{user.username}"''', (user.photo,))

        Database.save_database()

    @staticmethod
    def create_new_book(new_book: Book):
        if new_book.photo is None:
            Database.__db_con_cursor.execute(f'''INSERT INTO books
            (ISBN, name, author, holders, genres, price, about, is_unavailable, photo, date_time_added)
            VALUES ("{new_book.ISBN}", "{new_book.name}", 
            "{new_book.author}", "{new_book.holders}", "{new_book.genres}", 
            "{new_book.price}", "{new_book.about}", {new_book.is_unavailable}, NULL, "{new_book.date_time_added}");''')
        else:
            Database.__db_con_cursor.execute(f'''INSERT INTO books
            (ISBN, name, author, holders, genres, price, about, is_unavailable, photo, date_time_added)
            VALUES ("{new_book.ISBN}", "{new_book.name}", 
            "{new_book.author}", "{new_book.holders}", "{new_book.genres}",
            "{new_book.price}", "{new_book.about}", {new_book.is_unavailable},
             %s, "{new_book.date_time_added}");''', (new_book.photo,))

        Database.__db_con_cursor.execute(f'''INSERT INTO books_ratings(ISBN, ratings)
        VALUES ("{new_book.ISBN}", "{{}}")''')

        Database.save_database()

    @staticmethod
    def update_book(book: Book):
        if book.photo is None:
            Database.__db_con_cursor.execute(f'''UPDATE books
            SET name="{book.name}", author="{book.author}", genres="{book.genres}", 
            price="{book.price}", is_unavailable={book.is_unavailable}, about="{book.about}", photo=NULL
            WHERE ISBN="{book.ISBN}"''')
        else:
            Database.__db_con_cursor.execute(f'''UPDATE books
            SET name="{book.name}", author="{book.author}", genres="{book.genres}", 
            price="{book.price}", is_unavailable={book.is_unavailable}, about="{book.about}", photo=%s
            WHERE ISBN="{book.ISBN}"''', (book.photo,))

        Database.save_database()

    @staticmethod
    def update_book_holders(holders, isbn):
        Database.__db_con_cursor.execute(f'UPDATE books SET holders="{holders}" WHERE ISBN="{isbn}"')

        Database.save_database()

    @staticmethod
    def update_book_ratings(book_ratings: BookRatings):
        Database.__db_con_cursor.execute(f'''UPDATE books_ratings
        SET ratings="{book_ratings.ratings}" 
        WHERE ISBN="{book_ratings.ISBN}"''')

        Database.save_database()

    @staticmethod
    def get_user_by_username(username):
        tbr = Database.__filter_users(f'SELECT * FROM users WHERE username="{username}"')
        if not tbr:
            return None
        else:
            return tbr[0]

    @staticmethod
    def get_book_by_isbn(isbn):
        tbr = Database.__filter_books(f'SELECT * FROM books WHERE ISBN="{isbn}"')
        if not tbr:
            return None
        else:
            return tbr[0]

    @staticmethod
    def get_all_users():
        return Database.__filter_users(f'SELECT * FROM users')

    @staticmethod
    def __filter_users(sql):
        tbr = []
        Database.__db_con_cursor.execute(sql)
        users = list(Database.__db_con_cursor.fetchall())
        for i in users:
            tba = User(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
            tbr.append(tba)

        return tbr

    @staticmethod
    def get_all_books():
        return Database.__filter_books(f'SELECT * FROM books')

    @staticmethod
    def __filter_books(sql):
        tbr = []

        Database.__db_con_cursor.execute(sql)
        books = list(Database.__db_con_cursor.fetchall())
        for i in books:
            tba = Book(i[0], i[1], i[2], literal_eval(i[3]), literal_eval(i[4]), i[5], i[6], i[7], i[8], i[9])
            tbr.append(tba)

        return tbr

    @staticmethod
    def get_user_account_settings(username):
        Database.__db_con_cursor.execute(f'SELECT * FROM account_settings WHERE username="{username}"')
        s = list(Database.__db_con_cursor.fetchall())[0]
        return UserSettings(s[0], s[1], s[2])

    @staticmethod
    def update_user_account_settings(user_settings: UserSettings):
        Database.__db_con_cursor.execute(f'''UPDATE account_settings 
                             SET theme="{user_settings.theme}", accent_colour="{user_settings.accent_colour}" 
                             WHERE username="{user_settings.username}" ''')

        Database.save_database()

    @staticmethod
    def get_book_ratings(isbn):
        Database.__db_con_cursor.execute(f'SELECT * FROM books_ratings WHERE ISBN="{isbn}"')
        s = list(Database.__db_con_cursor.fetchall())[0]
        return BookRatings(s[0], literal_eval(s[1]))

    @staticmethod
    def set_book_ratings(book_ratings: BookRatings):
        Database.__db_con_cursor.execute(f'''UPDATE books_ratings 
                             SET ratings="{book_ratings.ratings}"
                             WHERE ISBN="{book_ratings.ISBN}" ''')

        Database.save_database()

    @staticmethod
    def save_database():
        Database.__db_con.commit()

    @staticmethod
    def save_local_database():
        Database.__local_db_con.commit()

    @staticmethod
    def is_new_local_setup():
        return len(list(Database.__local_db_con_cursor.execute(
            'SELECT name FROM sqlite_master WHERE type="table" AND name="local_settings";'))) == 0

    @staticmethod
    def is_new_server_setup():
        Database.__db_con_cursor.execute('SHOW TABLES LIKE "users"')
        return not Database.__db_con_cursor.fetchone()

    @staticmethod
    def delete_user(username):
        Database.__db_con_cursor.execute(f'DELETE FROM users WHERE username="{username}"')
        Database.__db_con_cursor.execute(f'DELETE FROM account_settings WHERE username="{username}"')

        Database.save_database()

        for each_book in Database.get_all_books():
            each_book.holders[:] = [x for x in each_book.holders if not x[0] == username]
            Database.update_book_holders(each_book.holders, each_book.ISBN)

            each_book_ratings = Database.get_book_ratings(each_book.ISBN)
            each_book_ratings.ratings.pop(username, None)
            Database.update_book_ratings(each_book_ratings)

    @staticmethod
    def delete_book(ISBN):
        Database.__db_con_cursor.execute(f'DELETE FROM books WHERE ISBN="{ISBN}"')
        Database.__db_con_cursor.execute(f'DELETE FROM books_ratings WHERE ISBN="{ISBN}"')

        Database.save_database()

    @staticmethod
    def delete_database():
        Database.__db_con_cursor.execute('DROP DATABASE snakebrary')

        Database.save_database()

    @staticmethod
    def delete_local_database():
        Database.__local_db_con_cursor.execute('DROP TABLE local_settings')

        Database.save_local_database()

    @staticmethod
    def get_random_book():
        tbr = Database.__filter_books(f'SELECT * FROM books ORDER BY RAND() LIMIT 1')
        if not tbr:
            return None
        else:
            return tbr[0]

    @staticmethod
    def clear_local_connection_settings():
        Database.set_local_connection_settings('', '', '', '')

    @staticmethod
    def set_local_connection_settings(host, port, user, password):
        Database.set_local_database_server_host(host)
        Database.set_local_database_server_port(port)
        Database.set_local_database_server_user(user)
        Database.set_local_database_server_password(password)

    @staticmethod
    def is_local_connection_settings_clear():
        return Database.get_local_database_server_host() == ''
