from logic.book import Book
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QPushButton, QWidget

from logic.database import Database
from window.helpers.enhanced_controls import LineEdit

class AdminAddBook(QWidget):

    def __init__(self, on_success, parent=None):
        super(AdminAddBook, self).__init__(parent)

        self.setWindowTitle('Add new Book')
        self.setFixedSize(500, 500)

        self.on_success = on_success

        self.new_book_name_field = LineEdit('Name')
        self.new_book_author_field = LineEdit('Author')
        self.new_book_isbn_field = LineEdit('ISBN')
        self.new_book_genre_field = LineEdit('Genre (Seperate with comma)')
        self.new_book_price_field = LineEdit('Price (₹)')

        self.proceed_button = QPushButton('Proceed')
        self.proceed_button.clicked.connect(self.on_proceed_button_clicked)

        # Create layout and add widgets

        vbox = QVBoxLayout()

        vbox.addLayout(self.new_book_name_field)
        vbox.addLayout(self.new_book_author_field)
        vbox.addLayout(self.new_book_isbn_field)
        vbox.addLayout(self.new_book_genre_field)
        vbox.addLayout(self.new_book_price_field)
        vbox.addWidget(self.proceed_button)

        self.setLayout(vbox)

    def on_proceed_button_clicked(self):
        proposed_new_book_name = self.new_book_name_field.line_edit.text()
        proposed_new_book_author = self.new_book_author_field.line_edit.text()
        proposed_new_book_isbn = self.new_book_isbn_field.line_edit.text()
        proposed_new_book_genre = self.new_book_genre_field.line_edit.text()
        proposed_new_book_price = self.new_book_price_field.line_edit.text()

        error = False

        if len(proposed_new_book_name) < 1:
            self.new_book_name_field.on_error('Too short!')
            error = True
        else:
            self.new_book_name_field.on_success()
        
        if len(proposed_new_book_author) < 1:
            self.new_book_author_field.on_error('Too short!')
            error = True
        else:
            self.new_book_author_field.on_success()
        
        if len(proposed_new_book_isbn) > 13:
            self.new_book_isbn_field.on_error('Invalid ISBN!')
            error = True
        else:
            self.new_book_isbn_field.on_success()
        
        if len(proposed_new_book_genre) < 1:
            self.new_book_genre_field.on_error('Too short!')
            error = True
        else:
            self.new_book_genre_field.on_success()

        if not proposed_new_book_price.isnumeric():
            self.new_book_price_field.on_error('Invalid price!')
            error = True
        else:
            self.new_book_price_field.on_success()

        if error:
            return

        self.set_disable(True)

        genres = proposed_new_book_genre.split(',')
        for i in range(len(genres)):
            genres[i] = genres[i].strip().lower()

        new_new_book = Book(proposed_new_book_isbn, proposed_new_book_name,
                                 proposed_new_book_author, '', [], genres, proposed_new_book_price)

        new_new_book.print_details()

        Database.create_new_book(new_new_book)
        Database.print_all_books()

        QMessageBox.information(self, 'Congratulations', 'New book has been added', QMessageBox.Ok)

        self.on_success()

    def set_disable(self, disable):
        self.proceed_button.setDisabled(disable)
        self.new_book_isbn_field.line_edit.setReadOnly(disable)
        self.new_book_name_field.line_edit.setReadOnly(disable)
        self.new_book_author_field.line_edit.setReadOnly(disable)
        self.new_book_genre_field.line_edit.setReadOnly(disable)
        self.new_book_price_field.line_edit.setReadOnly(disable)
