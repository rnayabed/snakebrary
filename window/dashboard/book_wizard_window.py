from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from logic.book import Book
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QPushButton, QWidget

from logic.database import Database
from window.helpers.enhanced_controls import FilePicker, ImageView, LineEdit, PlainTextEdit

class BookWizardWindowMode:
    ADD = 1,
    EDIT = 2

class BookWizardWindow(QDialog):

    def __init__(self, on_success, old_book=None, parent=None):
        super(BookWizardWindow, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.resize(700, 500)

        self.on_success = on_success

        self.new_book_cover_photo_path_field = FilePicker('Cover Picture (Optional)', on_select=self.on_cover_photo_selected, on_clear=self.on_cover_photo_cleared)

        self.new_book_cover_photo_preview = ImageView('Preview will appear here', 300, 300)

        self.photo_hbox = QHBoxLayout()
        self.photo_hbox.addWidget(self.new_book_cover_photo_path_field)
        self.photo_hbox.addWidget(self.new_book_cover_photo_preview)

        self.new_book_name_field = LineEdit('Name')
        self.new_book_author_field = LineEdit('Author')
        self.new_book_isbn_field = LineEdit('ISBN')
        self.new_book_genres_field = LineEdit('Genres (Seperate with comma)')
        self.new_book_price_field = LineEdit('Price (₹)')
        self.new_book_about_field = PlainTextEdit('About (Optional)')

        self.proceed_button = QPushButton('Proceed')
        self.proceed_button.clicked.connect(self.on_proceed_button_clicked)

        # Create layout and add widgets

        vbox = QVBoxLayout()
        
        vbox.addLayout(self.photo_hbox)
        vbox.addWidget(self.new_book_name_field)
        vbox.addWidget(self.new_book_author_field)
        vbox.addWidget(self.new_book_isbn_field)
        vbox.addWidget(self.new_book_genres_field)
        vbox.addWidget(self.new_book_price_field)
        vbox.addWidget(self.new_book_about_field)
        vbox.addWidget(self.proceed_button)

        self.setLayout(vbox)


        if old_book == None:
            self.setWindowTitle('Add Book')
            self.mode = BookWizardWindowMode.ADD
        else:
            self.setWindowTitle('Edit Book')
            self.old_book = old_book
            self.load_values_for_old_book()
            self.mode = BookWizardWindowMode.EDIT
            self.new_book_isbn_field.line_edit.setReadOnly(True)

    
    def load_values_for_old_book(self):
        if self.old_book.photo != None:
            self.new_book_cover_photo_preview.set_image_from_blob(self.old_book.photo)

        self.new_book_name_field.line_edit.setText(self.old_book.name)
        self.new_book_author_field.line_edit.setText(self.old_book.author)
        self.new_book_isbn_field.line_edit.setText(self.old_book.ISBN)
        self.new_book_genres_field.line_edit.setText((', '.join(self.old_book.genres)))
        self.new_book_price_field.line_edit.setText(str(self.old_book.price))
        self.new_book_about_field.plain_text_edit.setPlainText(self.old_book.about)

    def on_cover_photo_selected(self, img_path):
        self.new_book_cover_photo_preview.set_image_from_path(img_path)
            
    def on_cover_photo_cleared(self):
        self.new_book_cover_photo_path_field.line_edit.clear()
        self.new_book_cover_photo_preview.clear_image()

    def on_proceed_button_clicked(self):
        proposed_new_book_cover_photo_path = self.new_book_cover_photo_path_field.line_edit.text()
        proposed_new_book_name = self.new_book_name_field.line_edit.text()
        proposed_new_book_author = self.new_book_author_field.line_edit.text()
        proposed_new_book_isbn = self.new_book_isbn_field.line_edit.text()
        proposed_new_book_genres = self.new_book_genres_field.line_edit.text()
        proposed_new_book_price = self.new_book_price_field.line_edit.text()
        proposed_new_book_about = self.new_book_about_field.plain_text_edit.toPlainText()

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
        
        if len(proposed_new_book_isbn) > 13 or len(proposed_new_book_isbn) < 1:
            self.new_book_isbn_field.on_error('Invalid ISBN!')
            error = True
        else:
            self.new_book_isbn_field.on_success()
        
        if len(proposed_new_book_genres) < 1:
            self.new_book_genres_field.on_error('Too short!')
            error = True
        else:
            self.new_book_genres_field.on_success()
        
        try:
            float(proposed_new_book_price)
            self.new_book_price_field.on_success()
        except ValueError:
            self.new_book_price_field.on_error('Invalid price!')
            error = True

        if error:
            return

        self.set_disable(True)

        genres = proposed_new_book_genres.split(',')
        for i in range(len(genres)):
            genres[i] = genres[i].strip().lower()

        
        new_book = Book(proposed_new_book_isbn, proposed_new_book_name,
                        proposed_new_book_author, [], genres, proposed_new_book_price, 
                        proposed_new_book_about)


        if proposed_new_book_cover_photo_path != '':
            file = open(proposed_new_book_cover_photo_path, 'rb')
            new_book.photo = file.read()
            file.close()
        else:
            if self.mode == BookWizardWindowMode.EDIT and self.new_book_cover_photo_preview.is_clear == False:
                new_book.photo = self.old_book.photo


        if self.mode == BookWizardWindowMode.ADD:
            old_books = Database.get_books_by_ISBN(proposed_new_book_isbn)
            if len(old_books) > 0:
                QMessageBox.critical(None, 'Error', f'''Book with same ISBN already exists.
Name: {old_books[0].name}
Author: {old_books[0].author}
Price: {old_books[0].price}''', QMessageBox.Ok)
                return
            Database.create_new_book(new_book)

            close_message = 'Book was successfully added!'
        elif self.mode == BookWizardWindowMode.EDIT:
            new_book.holders = self.old_book.holders
            Database.update_book(new_book)
            close_message = 'Book was successfully edited!'
            
        
        self.on_success()
        QMessageBox.information(self, 'Congratulations', close_message, QMessageBox.Ok)
        self.close()

    def set_disable(self, disable):
        self.proceed_button.setDisabled(disable)
        self.new_book_isbn_field.line_edit.setReadOnly(disable)
        self.new_book_name_field.line_edit.setReadOnly(disable)
        self.new_book_author_field.line_edit.setReadOnly(disable)
        self.new_book_genres_field.line_edit.setReadOnly(disable)
        self.new_book_price_field.line_edit.setReadOnly(disable)
        self.new_book_about_field.plain_text_edit.setReadOnly(disable)
