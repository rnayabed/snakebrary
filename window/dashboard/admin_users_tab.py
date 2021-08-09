from window.dashboard.admin_add_user import AdminAddUser
from window.helpers.helpers import center_screen
from PySide6 import QtWidgets
from PySide6.QtWidgets import QAbstractScrollArea, QHeaderView, QLabel, QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QTableWidgetItem

from logic.database import Database
from logic.user import UserPrivilege, User


class AdminUsersTab(QWidget):

    def __init__(self, current_user:User, parent=None):
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
        
        #self.users_table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(button_bar)
        layout.addWidget(self.users_table)

        self.setLayout(layout)
        self.configure_users_table()

    def add_new_user(self, user_privilege):
        new_user_window = AdminAddUser(user_privilege, self.configure_users_table)
        new_user_window.show()
        center_screen(new_user_window)

    def configure_users_table(self):
        l_users = Database.get_all_users()

        self.users_table.clear()
        self.users_table.setRowCount(len(l_users))
        self.users_table.setColumnCount(4) 
        self.users_table.setHorizontalHeaderLabels(["Name", " Username ", " Privilege ", "Actions"])

        self.users_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        
        self.users_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.users_table.verticalHeader().setDefaultSectionSize(70)

        j = 0
        for i in l_users:
            name_item = QLabel(i.name)
            username_item = QLabel(i.username)

            print('asdaskdjankdjas', i.privilege)
            if i.privilege == UserPrivilege.NORMAL:
                p_text = 'Normal'
            elif i.privilege == UserPrivilege.ADMIN:
                p_text = 'Administrator'
            else:
                p_text = 'Master'

            privilege_item = QLabel(p_text)


            self.users_table.setCellWidget(j, 0, name_item)
            self.users_table.setCellWidget(j, 1, username_item)
            self.users_table.setCellWidget(j, 2, privilege_item)
            self.users_table.setCellWidget(j, 3, self.get_actions_bar_each_row(i))
            #self.users_table.resizeColumnsToContents()
            j += 1

        #self.users_table.resizeColumnsToContents

    def get_actions_bar_each_row(self, user:User):
        final_widget = QWidget()
        l = QHBoxLayout()

        delete_user_button = QPushButton('Delete')
        delete_user_button.clicked.connect(lambda: self.delete_user(user.username))
        delete_user_button.setProperty('class', 'danger')
        delete_user_button.setProperty('flat', 'true')

        edit_user_button = QPushButton(' Edit ')
        edit_user_button.setProperty('flat', 'true')

        view_info_button = QPushButton(' More Info  ')
        view_info_button.setProperty('flat', 'true')

        l.addWidget(view_info_button)
        l.addWidget(edit_user_button)
        l.addWidget(delete_user_button)

        if(user.username == self.current_user.username):
            delete_user_button.setEnabled(False)

        if(user.privilege == UserPrivilege.MASTER and self.current_user.privilege == UserPrivilege.ADMIN):
            edit_user_button.setEnabled(False)
            delete_user_button.setEnabled(False)

        final_widget.setLayout(l)
        return final_widget
    
    def delete_user(self, username):
        Database.delete_user(username)
        self.configure_users_table()
    