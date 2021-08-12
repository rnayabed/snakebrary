from window.dashboard.admin_add_user import AdminAddUser
from window.helpers.helpers import center_screen
from PySide6 import QtWidgets
from PySide6.QtWidgets import QAbstractScrollArea, QHeaderView, QLabel, QMessageBox, QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QTableWidgetItem

from logic.database import Database
from logic.user import UserPrivilege, User
from window.helpers.enhanced_controls import LineEdit

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
        
        self.search_bar = LineEdit('Search for user')
        self.search_bar.line_edit.textEdited.connect(self.search_bar_value_changed)


        layout.addLayout(button_bar)
        layout.addLayout(self.search_bar)
        layout.addWidget(self.users_table)

        self.setLayout(layout)
        self.configure_users_table()
    
    def search_bar_value_changed(self):
        search = self.search_bar.line_edit.text().lower()

        for i in range(self.users_table.rowCount()):
            name = self.users_table.cellWidget(i, 0).text().lower()

            if not search in name:
                self.users_table.hideRow(i)
            else:
                self.users_table.showRow(i)



    def add_new_user(self, user_privilege):
        new_user_window = AdminAddUser(user_privilege, self.configure_users_table)
        new_user_window.show()
        center_screen(new_user_window)

    def configure_users_table(self):
        l_users = Database.get_all_users()

        self.users_table.clear()
        self.users_table.setSortingEnabled(True)
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

            privilege_item = QLabel(UserPrivilege.get_ui_name(i.privilege))


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

        view_info_button = QPushButton(' More Info  ')
        view_info_button.setProperty('flat', 'true')

        l.addWidget(view_info_button)
        l.addWidget(delete_user_button)

        if(user.username == self.current_user.username):
            delete_user_button.setEnabled(False)

        if(user.privilege == UserPrivilege.MASTER and self.current_user.privilege == UserPrivilege.ADMIN):
            delete_user_button.setEnabled(False)

        final_widget.setLayout(l)
        return final_widget
    
    def delete_user(self, username):
        user_req = Database.get_users_by_username(username)[0]
        warning_box = QMessageBox.warning(self, 'Warning', f'''Are you sure you want to delete the following user
Name: {user_req.name}
Username: {user_req.username}''', QMessageBox.Yes, QMessageBox.No)

        if warning_box == QMessageBox.Yes:
            Database.delete_user(username)
            self.configure_books_table()
    