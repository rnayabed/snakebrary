from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.window.dashboard.settings_tab.about import About
from ui.window.dashboard.settings_tab.account_tab import AccountTab
from ui.window.dashboard.settings_tab.general_tab import GeneralTab


class SettingsTab(QWidget):

    def __init__(self, current_user, current_user_settings, dashboard_on_user_edited):
        super(SettingsTab, self).__init__()

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(GeneralTab(current_user, current_user_settings), 'General')
        self.account_tab = AccountTab(current_user, dashboard_on_user_edited)
        tabs.addTab(self.account_tab, 'Account')
        tabs.addTab(About(), 'About')
        layout.addWidget(tabs)

        self.setLayout(layout)
