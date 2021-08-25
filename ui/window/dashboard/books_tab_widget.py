from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QTableWidget, QPushButton

from logic.database import Database
from logic.user import UserPrivilege, User
from ui.helpers.enhanced_controls import LineEdit
from ui.helpers.helpers import FontAwesomeIcon, center_screen, get_font_size
from ui.window.book_info import BookInfo
from ui.window.book_wizard_window import BookWizardWindow


class BooksTabWidget(QWidget):

    def __init__(self, current_user: User, parent=None):
        super(BooksTabWidget, self).__init__(parent)

        self.current_user = current_user

        layout = QVBoxLayout()

        button_bar = QHBoxLayout()
        
        self.add_book_button = QPushButton(FontAwesomeIcon.PLUS+'New Book')
        self.add_book_button.clicked.connect(self.add_new_book)

        self.reload_button = QPushButton(FontAwesomeIcon.REFRESH+'Reload')
        self.reload_button.clicked.connect(self.reload_button_clicked)

        button_bar.addWidget(self.add_book_button)
        button_bar.addWidget(self.reload_button)

        self.books_table = QTableWidget()
        self.books_table.clicked.connect(self.books_table_clicked)

        self.search_bar = LineEdit('Search for book')
        self.search_bar.line_edit.textEdited.connect(self.search_bar_value_changed)
        self.search_bar.line_edit.setPlaceholderText('Search by Name, Author, Genre or ISBN')

        self.get_random_book_button = QPushButton('I\'m feeling lucky!')
        self.get_random_book_button.clicked.connect(self.get_random_book)

        layout.addLayout(button_bar)

        self.books_widget = QWidget()
        books_widget_vbox = QVBoxLayout()
        books_widget_vbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
        books_widget_vbox.addWidget(self.search_bar)
        books_widget_vbox.addWidget(self.get_random_book_button)
        books_widget_vbox.addWidget(self.books_table)
        self.books_widget.setLayout(books_widget_vbox)

        layout.addWidget(self.books_widget)

        self.no_books_widget = QWidget()
        no_books_vbox = QVBoxLayout()
        no_books_vbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
        no_books_vbox.setAlignment(QtCore.Qt.AlignCenter)

        no_books_found_label = QLabel('No books found')
        no_books_found_label.setAlignment(QtCore.Qt.AlignCenter)
        no_books_found_label.setFont(get_font_size(18))

        self.no_books_non_admin_sub_heading_label = QLabel('Ask the administrator to add some books!')
        self.no_books_non_admin_sub_heading_label.setAlignment(QtCore.Qt.AlignCenter)

        self.no_books_admin_sub_heading_label = QLabel('Click on "New Book" to add one!')
        self.no_books_admin_sub_heading_label.setAlignment(QtCore.Qt.AlignCenter)

        no_books_vbox.addWidget(no_books_found_label)
        no_books_vbox.addWidget(self.no_books_non_admin_sub_heading_label)
        no_books_vbox.addWidget(self.no_books_admin_sub_heading_label)
        self.no_books_widget.setLayout(no_books_vbox)
        
        layout.addWidget(self.no_books_widget)

        self.setLayout(layout)
        self.configure_books_table()

        if self.current_user.privilege == UserPrivilege.NORMAL:
            self.add_book_button.hide()

    
    def reload_button_clicked(self):
        self.reload_button.setDisabled(True)
        QApplication.instance().processEvents()
        self.configure_books_table()
        self.reload_button.setDisabled(False)

    def search_bar_value_changed(self):
        search = self.search_bar.line_edit.text().lower()

        for i in range(self.books_table.rowCount()):
            book = self.books_table.cellWidget(i, 0).property('book_obj')
            if not search in (book.name.lower() + book.author.lower() + ''.join(book.genres) + book.ISBN.lower()):
                self.books_table.hideRow(i)
            else:
                self.books_table.showRow(i)

    def add_new_book(self):
        self.new_book_window = BookWizardWindow(self.configure_books_table)
        self.new_book_window.exec()
        center_screen(self.new_book_window)

    def configure_books_table(self):
        l_books = Database.get_all_books()

        self.books_table.clear()
        self.books_table.setSortingEnabled(True)
        self.books_table.setRowCount(len(l_books))
        self.books_table.setColumnCount(3)
        self.books_table.setHorizontalHeaderLabels(["Name", "Author", "Genre"])

        self.books_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.books_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.books_table.verticalHeader().setDefaultSectionSize(70)

        if len(l_books) == 0:
            self.books_widget.hide()

            if self.current_user.privilege == UserPrivilege.NORMAL:
                self.no_books_non_admin_sub_heading_label.show()
                self.no_books_admin_sub_heading_label.hide()
            else:
                self.no_books_non_admin_sub_heading_label.hide()
                self.no_books_admin_sub_heading_label.show()

            self.no_books_widget.show()
        else:
            self.books_widget.show()
            self.no_books_widget.hide()

        for i in range(len(l_books)):
            each_book = l_books[i]
            name_widget = QLabel(each_book.name)
            author_widget = QLabel(each_book.author)
            genre_widget = QLabel(each_book.get_stylish_genres())

            name_widget.setProperty('book_obj', each_book)
            author_widget.setProperty('book_obj', each_book)
            genre_widget.setProperty('book_obj', each_book)

            self.books_table.setCellWidget(i, 0, name_widget)
            self.books_table.setCellWidget(i, 1, author_widget)
            self.books_table.setCellWidget(i, 2, genre_widget)

    def books_table_clicked(self, index):
        book = self.books_table.cellWidget(index.row(), index.column()).property('book_obj')
        self.open_book_info(book)
    
    def get_random_book(self):
        book = Database.get_random_book()
        self.open_book_info(book)
    
    def open_book_info(self, book):
        self.book_info_window = BookInfo(book, self.configure_books_table, self.current_user, self)
        self.book_info_window.exec()
        center_screen(self.book_info_window)
