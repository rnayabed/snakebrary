
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from window.dashboard.settings_tab.account_tab import AccountTab
from window.dashboard.settings_tab.general_tab import GeneralTab


class SettingsTab(QWidget):

    def __init__(self, app, current_user_settings):
        super(SettingsTab, self).__init__()


        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(GeneralTab(app, current_user_settings), 'General')
        self.tabs.addTab(AccountTab(), 'Account')
        layout.addWidget(self.tabs)

        self.setLayout(layout)


