from PySide6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QMessageBox)

from PySide6.QtCore import Qt

from window.helpers.helpers import get_font_size, center_screen
from window.helpers.new_user_layout import NewUserLayout

from logic.user import UserPrivilege


class AdminAddUser(QWidget):

    def __init__(self, new_user_privilege:UserPrivilege, on_success, parent=None):
        super(AdminAddUser, self).__init__(parent)

        self.setWindowTitle('Add new User')
        self.setFixedSize(500, 500)

        self.setLayout(NewUserLayout(on_success=self.on_success, user_privilege=new_user_privilege))
        self.on_success = on_success

    def on_success(self):
        self.on_success()
        QMessageBox.information(self, 'Congratulations', 'Account was successfully added!', QMessageBox.Ok)
        self.close()