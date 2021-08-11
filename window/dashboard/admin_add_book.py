from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from logic.book import Book
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QPushButton, QWidget

from logic.database import Database
from window.helpers.enhanced_controls import FilePicker, LineEdit

class AdminAddBook(QWidget):

    def __init__(self, on_success, parent=None):
        super(AdminAddBook, self).__init__(parent)

        self.setWindowTitle('Add new Book')
        self.resize(500, 500)

        self.on_success = on_success

        self.new_book_cover_photo_path_field = FilePicker('Cover Picture (Optional)', on_select=self.on_cover_photo_selected, on_clear=self.on_cover_photo_cleared)

        self.preview_will_appear_here_text = 'Preview will appear here'
        self.new_book_cover_photo_preview = QLabel(self.preview_will_appear_here_text)
        self.new_book_cover_photo_preview.setStyleSheet('border: 2px solid black;')
        self.new_book_cover_photo_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.new_book_cover_photo_preview.setFixedSize(200,200)

        self.photo_hbox = QHBoxLayout()
        self.photo_hbox.addLayout(self.new_book_cover_photo_path_field)
        self.photo_hbox.addWidget(self.new_book_cover_photo_preview)

        self.new_book_name_field = LineEdit('Name')
        self.new_book_author_field = LineEdit('Author')
        self.new_book_isbn_field = LineEdit('ISBN')
        self.new_book_genre_field = LineEdit('Genre (Seperate with comma)')
        self.new_book_price_field = LineEdit('Price (₹)')

        self.proceed_button = QPushButton('Proceed')
        self.proceed_button.clicked.connect(self.on_proceed_button_clicked)

        # Create layout and add widgets

        vbox = QVBoxLayout()
        
        vbox.addLayout(self.photo_hbox)
        vbox.addLayout(self.new_book_name_field)
        vbox.addLayout(self.new_book_author_field)
        vbox.addLayout(self.new_book_isbn_field)
        vbox.addLayout(self.new_book_genre_field)
        vbox.addLayout(self.new_book_price_field)
        vbox.addWidget(self.proceed_button)

        self.setLayout(vbox)

    def on_cover_photo_selected(self, img_path):
        pixmap = QPixmap(img_path).scaled(200,200, QtCore.Qt.KeepAspectRatio)
        self.new_book_cover_photo_preview.setPixmap(pixmap)
            
    def on_cover_photo_cleared(self):
        self.new_book_cover_photo_path_field.line_edit.clear()
        self.new_book_cover_photo_preview.clear()
        self.new_book_cover_photo_preview.setText(self.preview_will_appear_here_text)

    def on_proceed_button_clicked(self):
        proposed_new_book_cover_photo_path = self.new_book_cover_photo_path_field.line_edit.text()
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
        
        try:
            float(proposed_new_book_price)
            self.new_book_price_field.on_success()
        except ValueError:
            self.new_book_price_field.on_error('Invalid price!')
            error = True

        if error:
            return

        self.set_disable(True)

        genres = proposed_new_book_genre.split(',')
        for i in range(len(genres)):
            genres[i] = genres[i].strip().lower()

        new_book = Book(proposed_new_book_isbn, proposed_new_book_name,
                                 proposed_new_book_author, '', [], genres, proposed_new_book_price)

        if proposed_new_book_cover_photo_path != '':
            file = open(proposed_new_book_cover_photo_path, 'rb')
            new_book.photo = file.read()
            file.close()

        new_book.print_details()

        Database.create_new_book(new_book)
        Database.print_all_books()

        self.on_success()
        QMessageBox.information(self, 'Congratulations', 'Book was successfully added!', QMessageBox.Ok)
        self.close()

    def set_disable(self, disable):
        self.proceed_button.setDisabled(disable)
        self.new_book_isbn_field.line_edit.setReadOnly(disable)
        self.new_book_name_field.line_edit.setReadOnly(disable)
        self.new_book_author_field.line_edit.setReadOnly(disable)
        self.new_book_genre_field.line_edit.setReadOnly(disable)
        self.new_book_price_field.line_edit.setReadOnly(disable)
