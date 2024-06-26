from PySide6 import QtCore
from PySide6.QtWidgets import QDialog

from logic.user import User
from ui.layouts_and_widgets.user_info_vbox import UserInfoVBox


class UserInfo(QDialog):

    def __init__(self, user: User, current_user: User, dashboard_on_user_edited=None, parent=None,
                 disable_edit_option=False):
        super(UserInfo, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle("User Information")
        self.setFixedHeight(320)

        self.user_info_vbox = UserInfoVBox(user, current_user, dashboard_on_user_edited, self,
                                           disable_edit_options=disable_edit_option)
        self.setLayout(self.user_info_vbox)
