from window.dashboard.book_ratings_layout import BookRatingsLayout
from logic.user import User
from logic.database import Database
from os import name
from window.helpers.helpers import get_font_size
from window.helpers.enhanced_controls import ImageView
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from logic.book import Book, BookHolder
from PySide6.QtWidgets import (QAbstractScrollArea, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools


class BookInfo(QScrollArea):

    def __init__(self, book: Book, current_user: User, parent=None):
        super(BookInfo, self).__init__(parent)

        self.book = book
        self.current_user = current_user

        self.setWindowTitle("Book Information")
        self.resize(800,600)


        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(QtCore.Qt.AlignTop)

        hbox_1 = QHBoxLayout()
        hbox_1.setSpacing(10)

        self.cover_photo = ImageView('Cover Photo', 300, 300)
        hbox_1.addWidget(self.cover_photo)

        self.name_label = QLabel()
        self.name_label.setFont(get_font_size(30))
        self.name_label.setStyleSheet('padding-bottom: 10px;')

        self.author_label = QLabel()
        self.author_label.setFont(get_font_size(20))

        self.genres_label = QLabel()

        self.isbn_label = QLabel()
        self.price_label = QLabel()

        self.get_return_button = QPushButton()


        vbox_labels_1 = QVBoxLayout()
        vbox_labels_1.setAlignment(QtCore.Qt.AlignTop)
        vbox_labels_1.addWidget(self.name_label)
        vbox_labels_1.addWidget(self.author_label)
        vbox_labels_1.addWidget(self.genres_label)
        vbox_labels_1.addWidget(self.isbn_label)
        vbox_labels_1.addWidget(self.price_label)
        vbox_labels_1.addWidget(self.get_return_button)

        hbox_1.addLayout(vbox_labels_1)


        main_vbox.addLayout(hbox_1)


        self.about_label_header = QLabel('About')
        self.about_label_header.setStyleSheet('padding-top: 10px;')
        self.about_label_header.setFont(get_font_size(18))
        self.about_label = QLabel()

        about_layout = QVBoxLayout()
        about_layout.addWidget(self.about_label_header)
        about_layout.addWidget(self.about_label)

        main_vbox.addLayout(about_layout)

        self.ratings_layout = BookRatingsLayout(self.book, self.current_user)

        main_vbox.addLayout(self.ratings_layout)

        widget = QWidget()
        widget.setLayout(main_vbox)
    
        self.setWidget(widget)
        self.setWidgetResizable(True)

        self.configure_ui()
    
    def configure_ui(self):

        if self.book.photo != None:
            self.cover_photo.set_image_from_blob(self.book.photo)
        
        self.name_label.setText(self.book.name)
        self.author_label.setText(f'by {self.book.author}')
        
        if len(self.book.genres) == 1:
            self.genres_label.setText('Genre: '+self.book.get_stylish_genres())
        else:
            self.genres_label.setText('Genres: '+self.book.get_stylish_genres())

        self.isbn_label.setText(f'ISBN: {self.book.ISBN}')
        self.price_label.setText(f'Price: ₹ {self.book.price}')

        if self.book.about != '':
            self.about_label.setText(self.book.about)
        else:
            self.about_label_header.hide()
            self.about_label.hide()


        self.configure_get_return_button()

    def get_button(self):
        new_holder = BookHolder(self.current_user.username)

        print('book holders before \n\n',self.book.holders)

        self.book.holders.append(new_holder.get_raw_list())

        print('book holders after \n\n',self.book.holders)

        Database.update_book(self.book)
        
        self.configure_get_return_button()
    
    def return_button(self):
        self.book.return_now()
        Database.update_book(self.book)

        self.configure_get_return_button()
        self.ratings_layout.book = self.book
        self.ratings_layout.configure_ui()
    
    def configure_get_return_button(self):
        if self.book.get_current_holder() == None:
            self.get_return_button.setText('Get it')
            self.get_return_button.clicked.connect(self.get_button)
        else:
            if self.book.get_current_holder() == self.current_user.username:
                self.get_return_button.setText('Return')
                self.get_return_button.clicked.connect(self.return_button)
            else:
                self.get_return_button.setDisabled(True)
                self.get_return_button.setText('Unavailable')
        
