from PySide2.QtWidgets import QWidget

from ui.layouts_and_widgets.user_info_vbox import UserInfoVBox


class AccountTab(QWidget):

    def __init__(self, current_user, dashboard_on_user_edited):
        super(AccountTab, self).__init__()

        self.current_user = current_user
        self.dashboard_on_user_edited = dashboard_on_user_edited

        self.user_info_vbox = UserInfoVBox(self.current_user, self.current_user, self.dashboard_on_user_edited, self, True)
        self.setLayout(self.user_info_vbox)
