from ui.window.user_info import UserInfo
from ui.helpers.helpers import FontAwesomeIcon, center_screen
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QTableWidget, QVBoxLayout, QWidget

from logic.database import Database


class BookHoldersWindow(QDialog):

    def __init__(self, book_holders, current_user, parent=None):
        super(BookHoldersWindow, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.book_holders = book_holders
        self.current_user = current_user

        self.setWindowTitle("Book Holders")
        self.resize(800, 600)

        self.book_holders_table = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.book_holders_table)

        self.setLayout(vbox)

        self.configure_holders_table()

    def configure_holders_table(self):
        self.book_holders_table.setSortingEnabled(True)
        self.book_holders_table.setRowCount(len(self.book_holders))
        self.book_holders_table.setColumnCount(5)
        self.book_holders_table.setHorizontalHeaderLabels(["Username", "Name", "   Issued On   ", "   Returned On   ", "          Action          "])

        self.book_holders_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.book_holders_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.book_holders_table.verticalHeader().setDefaultSectionSize(70)

        for i in range(len(self.book_holders)):
            each_holder = self.book_holders[i]

            user_obj = Database.get_user_by_username(each_holder[0])
            username_widget = QLabel(each_holder[0])
            name_widget = QLabel(user_obj.name)
            issued_on_widget = QLabel(each_holder[1])
            returned_on_widget = QLabel(each_holder[2])

            view_profile_button = QPushButton(FontAwesomeIcon.EYE+'View Profile')
            view_profile_button.setProperty('user_obj', user_obj)
            view_profile_button.clicked.connect(self.view_holder_profile)

            vbox = QVBoxLayout()
            vbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
            vbox.addWidget(view_profile_button)
          

            view_profile_button_widget = QWidget()
            view_profile_button_widget.setContentsMargins(QtCore.QMargins(0,0,0,0))
            view_profile_button_widget.setLayout(vbox)

            self.book_holders_table.setCellWidget(i, 0, username_widget)
            self.book_holders_table.setCellWidget(i, 1, name_widget)
            self.book_holders_table.setCellWidget(i, 2, issued_on_widget)
            self.book_holders_table.setCellWidget(i, 3, returned_on_widget)
            self.book_holders_table.setCellWidget(i, 4, view_profile_button_widget)

    def view_holder_profile(self):
        self.users_info_window = UserInfo(self.sender().property('user_obj'), self.current_user, self.configure_holders_table, self)
        self.users_info_window.exec()
        center_screen(self.users_info_window)