from ui.helpers.helpers import center_screen
from ui.window.user_info import UserInfo
from logic.user import User, UserPrivilege
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QTableWidget, QVBoxLayout, \
    QWidget
from shiboken6.Shiboken import delete

from logic.database import Database


class BookReviewersWindow(QDialog):

    def __init__(self, book, current_user, on_review_deleted, parent):
        super(BookReviewersWindow, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.book = book
        self.current_user = current_user
        self.on_review_deleted = on_review_deleted


        self.setWindowTitle("Book Reviewers")
        self.resize(800, 600)

        self.book_reviewers_table = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.book_reviewers_table)

        self.setLayout(vbox)

        self.configure_reviewers_table()

    def configure_reviewers_table(self):
        self.book_ratings = Database.get_book_ratings(self.book.ISBN)

        self.book_reviewers_table.clear()
        self.book_reviewers_table.setSortingEnabled(True)
        self.book_reviewers_table.setRowCount(len(self.book_ratings.ratings))
        self.book_reviewers_table.setColumnCount(4)
        self.book_reviewers_table.setHorizontalHeaderLabels(["Username", "Name", "Rating", "                           Actions                          "])

        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.book_reviewers_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.book_reviewers_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.book_reviewers_table.verticalHeader().setDefaultSectionSize(70)

        i = 0
        for each_reviewer in self.book_ratings.ratings.keys():
            username_widget = QLabel(each_reviewer)
            each_reviewer_user_obj = Database.get_user_by_username(each_reviewer)
            name_widget = QLabel(each_reviewer_user_obj.name)
            rating_widget = QLabel(str(self.book_ratings.ratings[each_reviewer]))

            delete_button = QPushButton('Delete')
            delete_button.setProperty('class', 'danger')
            delete_button.setProperty('username', each_reviewer)
            delete_button.clicked.connect(self.delete_rating)

            view_profile_button = QPushButton('View Profile')
            view_profile_button.setProperty('user_obj', each_reviewer_user_obj)
            view_profile_button.clicked.connect(self.view_reviewer_profile)

            hbox = QHBoxLayout()
            hbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
            hbox.addWidget(view_profile_button)
            if (self.current_user.privilege != each_reviewer_user_obj.privilege and each_reviewer_user_obj.privilege != UserPrivilege.MASTER) or self.current_user.username == each_reviewer:
                hbox.addWidget(delete_button)
            

            view_profile_delete_button_widget = QWidget()
            view_profile_delete_button_widget.setContentsMargins(QtCore.QMargins(0,0,0,0))
            view_profile_delete_button_widget.setLayout(hbox)

            self.book_reviewers_table.setCellWidget(i, 0, username_widget)
            self.book_reviewers_table.setCellWidget(i, 1, name_widget)
            self.book_reviewers_table.setCellWidget(i, 2, rating_widget)
            self.book_reviewers_table.setCellWidget(i, 3, view_profile_delete_button_widget)

            i += 1

    def view_reviewer_profile(self):
        self.users_info_window = UserInfo(self.sender().property('user_obj'), self.current_user,
                                          self.configure_reviewers_table, self, True)
        self.users_info_window.exec()
        center_screen(self.users_info_window)
    
    def delete_rating(self):
        self.book_ratings.ratings.pop(self.sender().property('username'), None)
        Database.update_book_ratings(self.book_ratings)
        self.configure_reviewers_table()
        self.on_review_deleted()
