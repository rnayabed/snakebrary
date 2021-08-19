from ui.helpers.enhanced_controls import LineEdit
from ui.helpers.helpers import center_screen
from ui.window.book_info import BookInfo
from ui.window.book_wizard_window import BookWizardWindow
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QTableWidget, QPushButton
from logic.database import Database
from logic.user import UserPrivilege, User


class BooksTabWidget(QWidget):

    def __init__(self, current_user: User, parent=None):
        super(BooksTabWidget, self).__init__(parent)

        self.current_user = current_user

        layout = QVBoxLayout()

        self.add_book_button = QPushButton('New Book')
        self.add_book_button.clicked.connect(self.add_new_book)

        self.books_table = QTableWidget()
        self.books_table.clicked.connect(self.books_table_clicked)
        
        self.search_bar = LineEdit('Search for book')
        self.search_bar.line_edit.textEdited.connect(self.search_bar_value_changed)
        self.search_bar.line_edit.setPlaceholderText('Search by Name, Author or ISBN')

        layout.addWidget(self.add_book_button)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.books_table)

        self.setLayout(layout)
        self.configure_books_table()

        if self.current_user.privilege == UserPrivilege.NORMAL:
            self.add_book_button.hide()
    
    def search_bar_value_changed(self):
        search = self.search_bar.line_edit.text().lower()

        for i in range(self.books_table.rowCount()):
            name = self.books_table.cellWidget(i, 0).text().lower()
            author = self.books_table.cellWidget(i, 1).text().lower()
            isbn = self.books_table.cellWidget(i, 2).text().lower()

            if not search in (name+author+isbn):
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
        self.book_info_window = BookInfo(book, self.configure_books_table, self.current_user, self)
        self.book_info_window.exec()
        center_screen(self.book_info_window)
    


    