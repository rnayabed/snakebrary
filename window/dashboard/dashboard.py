from window.dashboard.books_tab_widget import BooksTabWidget
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools

from logic.database import Database
from logic.user import User, UserPrivilege
from window.dashboard.admin_users_tab import AdminUsersTab
from window.dashboard.settings_tab.settings_tab import SettingsTab


class Dashboard(QWidget, QtStyleTools):

    def __init__(self, current_user: User, parent=None):
        super(Dashboard, self).__init__(parent)

        self.current_user = current_user
        self.current_user_account_settings = Database.get_user_account_settings(self.current_user.username)

        self.setWindowTitle(f'Snakebrary - Logged in as {self.current_user.username} ({self.current_user.name})')

        self.resize(1024, 768)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.configure_tabs()
        layout.addWidget(self.tabs)

        self.configure_theme_and_accent_colour()

        self.setLayout(layout)

    def configure_tabs(self):
        if self.current_user.privilege != UserPrivilege.NORMAL:
            self.admin_users_table = AdminUsersTab(self.current_user)
            self.tabs.addTab(self.admin_users_table, 'Users')
        

        self.tabs.addTab(BooksTabWidget(self.current_user), 'Books')

        self.tabs.addTab(SettingsTab(self.current_user, self.current_user_account_settings, self.dashboard_on_user_edited), "Settings")

    def configure_theme_and_accent_colour(self):
        stylesheet_name = f'{self.current_user_account_settings.theme.lower()}_{self.current_user_account_settings.accent_colour.lower().replace(" ", "")}.xml'

        print(stylesheet_name)
        apply_stylesheet(QApplication.instance(), stylesheet_name)

    def dashboard_on_user_edited(self):
        if self.current_user.privilege != UserPrivilege.NORMAL:
            self.admin_users_table.configure_users_table()
