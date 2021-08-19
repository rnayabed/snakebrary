from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from shiboken6.Shiboken import delete

from logic.database import Database


class BookReviewersWindow(QDialog):

    def __init__(self, book, current_user, on_review_deleted, parent):
        super(BookReviewersWindow, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.book = book
        self.current_user = current_user
        self.on_review_deleted = on_review_deleted

        self.book_ratings = Database.get_book_ratings(self.book.ISBN)

        self.setWindowTitle("Book Reviewers")
        self.resize(800, 600)

        self.book_reviewers_table = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.book_reviewers_table)

        self.setLayout(vbox)

        self.configure_reviewers_table()

    def configure_reviewers_table(self):
        self.book_reviewers_table.setSortingEnabled(True)
        self.book_reviewers_table.setRowCount(len(self.book_ratings.ratings))
        self.book_reviewers_table.setColumnCount(4)
        self.book_reviewers_table.setHorizontalHeaderLabels(["Username", "Name", "Rating", "  Action  "])

        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.book_reviewers_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.book_reviewers_table.verticalHeader().setDefaultSectionSize(70)

        i = 0
        for each_reviewer in self.book_ratings.ratings.keys():
            username_widget = QLabel(each_reviewer)
            name_widget = QLabel(Database.get_user_by_username(each_reviewer).name)
            rating_widget = QLabel(str(self.book_ratings.ratings[each_reviewer]))

            delete_button = QPushButton('Delete')
            delete_button.setProperty('class', 'danger')
            delete_button.clicked.connect(lambda: self.delete_rating(each_reviewer))

            vbox = QVBoxLayout()
            vbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
            vbox.addWidget(delete_button)

            delete_button_widget = QWidget()
            delete_button_widget.setContentsMargins(QtCore.QMargins(0,0,0,0))
            delete_button_widget.setLayout(vbox)

            self.book_reviewers_table.setCellWidget(i, 0, username_widget)
            self.book_reviewers_table.setCellWidget(i, 1, name_widget)
            self.book_reviewers_table.setCellWidget(i, 2, rating_widget)
            self.book_reviewers_table.setCellWidget(i, 3, delete_button_widget)

            i += 1
    
    def delete_rating(self, username):
        self.book_ratings.ratings.pop(username, None)
        Database.update_book_ratings(self.book_ratings)
        self.configure_reviewers_table()
        self.on_review_deleted()
