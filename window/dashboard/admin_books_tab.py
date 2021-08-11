from window.dashboard.admin_add_book import AdminAddBook
from logic.book import Book
from window.dashboard.admin_add_user import AdminAddUser
from window.helpers.helpers import center_screen
from PySide6 import QtWidgets
from PySide6.QtWidgets import QAbstractScrollArea, QHeaderView, QLabel, QMessageBox, QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QTableWidgetItem

from logic.database import Database
from logic.user import UserPrivilege, User
from window.helpers.enhanced_controls import LineEdit

class AdminBooksTab(QWidget):

    def __init__(self, current_user:User, parent=None):
        super(AdminBooksTab, self).__init__(parent)

        self.current_user = current_user

        layout = QVBoxLayout()

        self.add_book_button = QPushButton('New Book')
        self.add_book_button.clicked.connect(self.add_new_book)

        self.books_table = QTableWidget()
        
        self.search_bar = LineEdit('Search for book')
        self.search_bar.line_edit.textEdited.connect(self.search_bar_value_changed)

        layout.addWidget(self.add_book_button)
        layout.addLayout(self.search_bar)
        layout.addWidget(self.books_table)

        self.setLayout(layout)
        self.configure_books_table()
    
    def search_bar_value_changed(self):
        search = self.search_bar.line_edit.text().lower()

        for i in range(self.books_table.rowCount()):
            name = self.books_table.cellWidget(i, 0).text().lower()

            if not search in name:
                self.books_table.hideRow(i)
            else:
                self.books_table.showRow(i)

    def add_new_book(self):
        self.new_book_window = AdminAddBook(self.configure_books_table)
        self.new_book_window.show()
        center_screen(self.new_book_window)

    def configure_books_table(self):
        l_books = Database.get_all_books()

        self.books_table.clear()
        self.books_table.setSortingEnabled(True)
        self.books_table.setRowCount(len(l_books))
        self.books_table.setColumnCount(5) 
        self.books_table.setHorizontalHeaderLabels(["Name", "Author", "Current Holder", "Price (₹)", "Actions"])

        self.books_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        self.books_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.books_table.verticalHeader().setDefaultSectionSize(70)

        j = 0
        for i in l_books:
            name_item = QLabel(i.name)
            author_item = QLabel(i.author)

            c_holder = i.current_holder
            if c_holder == '':
                c_holder = 'No-one'


            current_holder_item = QLabel(c_holder)
            price_item = QLabel(str(i.price))


            self.books_table.setCellWidget(j, 0, name_item)
            self.books_table.setCellWidget(j, 1, author_item)
            self.books_table.setCellWidget(j, 2, current_holder_item)
            self.books_table.setCellWidget(j, 3, price_item)
            self.books_table.setCellWidget(j, 4, self.get_actions_bar_each_row(i))
            j += 1


    def get_actions_bar_each_row(self, book: Book):
        final_widget = QWidget()
        l = QHBoxLayout()

        delete_user_button = QPushButton('Delete')
        delete_user_button.clicked.connect(lambda: self.delete_book(book.ISBN))
        delete_user_button.setProperty('class', 'danger')
        delete_user_button.setProperty('flat', 'true')

        view_info_button = QPushButton(' More Info  ')
        view_info_button.setProperty('flat', 'true')

        l.addWidget(view_info_button)
        l.addWidget(delete_user_button)

        if(self.current_user.privilege == UserPrivilege.NORMAL):
            delete_user_button.setEnabled(False)

        final_widget.setLayout(l)
        return final_widget
    
    def delete_book(self, ISBN):
        book_req = Database.get_books_by_ISBN(ISBN)[0]
        warning_box = QMessageBox.warning(self, 'Warning', f'''Are you sure you want to delete the following book
Name: {book_req.name}
Author: {book_req.author}
ISBN: {book_req.ISBN}''', QMessageBox.Yes, QMessageBox.No)

        if warning_box == QMessageBox.Yes:
            Database.delete_book(ISBN)
            self.configure_books_table()

    