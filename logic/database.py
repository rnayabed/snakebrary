from logic.book import Book, BookReviews
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
        Database.create_new_books_table()
        Database.create_new_books_reviews_table()

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
    def create_new_books_table():
        global __db_con
        __db_con.execute('''CREATE TABLE books
        (ISBN   TEXT  PRIMARY KEY  NOT NULL,
        name    TEXT    NOT NULL,
        author   TEXT    NOT NULL,
        current_holder    TEXT    NOT NULL,
        previous_holders   TEXT NOT NULL,
        genre    TEXT    NOT_NULL,
        price   INT NOT_NULL,
        date_time_added    TEXT    NOT_NULL);''')

    @staticmethod
    def create_new_books_reviews_table():
        global __db_con
        __db_con.execute('''CREATE TABLE books_reviews
        (ISBN   TEXT  PRIMARY KEY  NOT NULL,
        ratings    TEXT    NOT NULL,
        reviews   TEXT    NOT NULL);''')


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
    def create_new_book(new_book: Book):
        global __db_con
        __db_con.execute(f'''INSERT INTO books(ISBN, name, author, current_holder, previous_holders, genre, price, date_time_added)
        VALUES ("{new_book.ISBN}", "{new_book.name}", 
        "{new_book.author}", "{new_book.current_holder}", "{new_book.previous_holders}",
        "{new_book.genre}", "{new_book.price}", "{new_book.date_time_added}");''')

        __db_con.execute(f'''INSERT INTO books_reviews(ISBN, ratings, reviews)
        VALUES ("{new_book.ISBN}", "0.0", "{{}}")''')

        __db_con.commit()

    @staticmethod
    def get_users_by_username(username):
        return Database.__filter_users(f'SELECT * FROM users WHERE username="{username}"')

    @staticmethod
    def get_books_by_ISBN(ISBN):
        return Database.__filter_users(f'SELECT * FROM books WHERE ISBN="{ISBN}"')

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
    def get_all_books():
        return Database.__filter_books(f'SELECT * FROM books')

    @staticmethod
    def __filter_books(sql):
        global __db_con
        __db_con.execute(sql)
        books = list(__db_con.execute(sql))

        tbr = []

        for i in books:
            tba = Book(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
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
        __db_con.execute(f'''UPDATE account_settings 
                             SET theme="{user_settings.theme}", accent_colour="{user_settings.accent_colour}" 
                             WHERE username="{user_settings.username}" ''')

        Database.save_database()
    
    @staticmethod
    def get_book_reviews(ISBN):
        global __db_con
        s = list(__db_con.execute(f'SELECT * FROM books_reviews WHERE ISBN="{ISBN}"'))[0]
        return BookReviews(s[0], s[1], s[2])

    @staticmethod
    def set_book_reviews(book_reviews: BookReviews):
        global __db_con
        __db_con.execute(f'''UPDATE book_reviews 
                             SET ratings="{book_reviews.ratings}", reviews="{book_reviews.reviews}" 
                             WHERE ISBN="{book_reviews.ISBN}" ''')

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
    def print_all_books():
        global __db_con
        print(list(__db_con.execute("SELECT * FROM books")))

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
    
    @staticmethod
    def delete_book(ISBN):
        global __db_con
        __db_con.execute(f'DELETE FROM books WHERE ISBN="{ISBN}"')
        __db_con.execute(f'DELETE FROM books_reviews WHERE ISBN="{ISBN}"')  

        Database.save_database()