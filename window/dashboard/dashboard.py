from PySide6.QtWidgets import (QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools

from logic.database import Database
from logic.user import User, UserPrivilege
from window.dashboard.admin_books_tab import AdminBooksTab
from window.dashboard.admin_users_tab import AdminUsersTab
from window.dashboard.settings_tab.settings_tab import SettingsTab


class Dashboard(QWidget, QtStyleTools):

    def __init__(self, current_user: User, app, parent=None):
        super(Dashboard, self).__init__(parent)

        self.app = app

        self.setWindowTitle("Snakebrary - Dashboard")

        self.resize(800, 600)

        self.current_user = current_user
        self.current_user_settings = Database.get_user_settings(self.current_user.username)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.configure_tabs()
        layout.addWidget(self.tabs)

        self.configure_theme_and_accent_colour()

        self.setLayout(layout)

    def configure_tabs(self):
        if self.current_user.privilege != UserPrivilege.NORMAL:
            self.tabs.addTab(AdminUsersTab(self.current_user), 'Users')
            self.tabs.addTab(AdminBooksTab(self.current_user), 'Books')

        self.tabs.addTab(SettingsTab(self.app, self.current_user_settings), "Settings")

    def configure_theme_and_accent_colour(self):
        stylesheet_name = f'{self.current_user_settings.theme.lower()}_{self.current_user_settings.accent_colour.lower().replace(" ", "")}.xml'

        print(stylesheet_name)
        apply_stylesheet(self.app, stylesheet_name)
