from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QLabel, QTableWidget, QVBoxLayout

from logic.database import Database


class BookReviewersWindow(QDialog):

    def __init__(self, book, current_user, parent=None):
        super(BookReviewersWindow, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.current_user = current_user
        self.book = book

        self.book_ratings = Database.get_book_ratings(self.book.ISBN)

        self.setWindowTitle("Book Reviewers")
        self.resize(800, 600)

        self.book_reviewers_table = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.book_reviewers_table)

        self.setLayout(vbox)

        self.configure_table()

    def configure_table(self):
        self.book_reviewers_table.setSortingEnabled(True)
        self.book_reviewers_table.setRowCount(len(self.book_ratings.ratings))
        self.book_reviewers_table.setColumnCount(3)
        self.book_reviewers_table.setHorizontalHeaderLabels(["Username", "Name", "Rating"])

        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.book_reviewers_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.book_reviewers_table.verticalHeader().setDefaultSectionSize(70)

        i = 0
        for each_reviewer in self.book_ratings.ratings.keys():
            username_widget = QLabel(each_reviewer)
            name_widget = QLabel(Database.get_user_by_username(each_reviewer).name)
            rating_widget = QLabel(str(self.book_ratings.ratings[each_reviewer]))

            self.book_reviewers_table.setCellWidget(i, 0, username_widget)
            self.book_reviewers_table.setCellWidget(i, 1, name_widget)
            self.book_reviewers_table.setCellWidget(i, 2, rating_widget)

            i += 1