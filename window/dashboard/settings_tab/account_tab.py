
from window.helpers.user_info_vbox import UserInfoVBox
from window.dashboard.user_info import UserInfo
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AccountTab(QWidget):

    def __init__(self, current_user, dashboard_on_user_edited):
        super(AccountTab, self).__init__()

        self.user_info_vbox = UserInfoVBox(current_user, current_user, dashboard_on_user_edited, self)
        self.setLayout(self.user_info_vbox)


