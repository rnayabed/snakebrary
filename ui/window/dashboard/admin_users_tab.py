from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout

from logic.database import Database
from logic.user import UserPrivilege, User
from ui.helpers.enhanced_controls import LineEdit
from ui.helpers.helpers import center_screen
from ui.window.add_user import AddUser
from ui.window.user_info import UserInfo


class AdminUsersTab(QWidget):

    def __init__(self, current_user: User, parent=None):
        super(AdminUsersTab, self).__init__(parent)

        self.current_user = current_user

        layout = QVBoxLayout()

        button_bar = QHBoxLayout()

        self.add_admin_button = QPushButton('New Admin user')
        self.add_admin_button.clicked.connect(lambda: self.add_new_user(UserPrivilege.ADMIN))

        self.add_normal_button = QPushButton('New Normal user')
        self.add_normal_button.clicked.connect(lambda: self.add_new_user(UserPrivilege.NORMAL))

        button_bar.addWidget(self.add_admin_button)
        button_bar.addWidget(self.add_normal_button)

        self.users_table = QTableWidget()
        self.users_table.clicked.connect(self.users_table_clicked)

        self.search_bar = LineEdit('Search for user')
        self.search_bar.line_edit.textEdited.connect(self.search_bar_value_changed)
        self.search_bar.line_edit.setPlaceholderText('Search by Name or Username')

        layout.addLayout(button_bar)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.users_table)

        self.setLayout(layout)

        if self.current_user.privilege == UserPrivilege.ADMIN:
            self.add_admin_button.hide()

        self.configure_users_table()

    def search_bar_value_changed(self):
        search = self.search_bar.line_edit.text().lower()

        for i in range(self.users_table.rowCount()):
            name = self.users_table.cellWidget(i, 0).text().lower()
            username = self.users_table.cellWidget(i, 1).text().lower()

            if not search in (name + username):
                self.users_table.hideRow(i)
            else:
                self.users_table.showRow(i)

    def add_new_user(self, user_privilege):
        new_user_window = AddUser(user_privilege, self.configure_users_table, self)
        new_user_window.exec()
        center_screen(new_user_window)

    def configure_users_table(self):
        l_users = Database.get_all_users()

        self.users_table.clear()
        self.users_table.setSortingEnabled(True)
        self.users_table.setRowCount(len(l_users))
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["Name", " Username ", " Privilege "])

        self.users_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.users_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.users_table.verticalHeader().setDefaultSectionSize(70)

        for i in range(len(l_users)):
            each_user = l_users[i]
            name_widget = QLabel(each_user.name)
            username_widget = QLabel(each_user.username)
            privilege_widget = QLabel(UserPrivilege.get_ui_name(each_user.privilege))

            name_widget.setProperty('user_obj', each_user)
            username_widget.setProperty('user_obj', each_user)
            privilege_widget.setProperty('user_obj', each_user)

            self.users_table.setCellWidget(i, 0, name_widget)
            self.users_table.setCellWidget(i, 1, username_widget)
            self.users_table.setCellWidget(i, 2, privilege_widget)

    def users_table_clicked(self, index):
        user = self.users_table.cellWidget(index.row(), index.column()).property('user_obj')
        self.users_info_window = UserInfo(user, self.current_user, self.configure_users_table, self)
        self.users_info_window.exec()
        center_screen(self.users_info_window)
