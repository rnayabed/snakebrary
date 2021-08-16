
from window.dashboard.settings_tab.about import About
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from window.dashboard.settings_tab.account_tab import AccountTab
from window.dashboard.settings_tab.general_tab import GeneralTab


class SettingsTab(QWidget):

    def __init__(self, logout, current_user_settings):
        super(SettingsTab, self).__init__()


        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(GeneralTab(logout, current_user_settings), 'General')
        self.tabs.addTab(AccountTab(), 'Account')
        self.tabs.addTab(About(), 'About')
        layout.addWidget(self.tabs)

        self.setLayout(layout)


