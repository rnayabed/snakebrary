from window.helpers.user_wizard import UserWizard
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QMessageBox)

from PySide6.QtCore import Qt

from window.helpers.helpers import get_font_size, center_screen

from logic.user import UserPrivilege


class EditUser(QWidget):

    def __init__(self, user, on_successful, parent=None):
        super(EditUser, self).__init__(parent)

        self.setWindowTitle('Add new User')
        self.setFixedSize(500, 500)

        self.setLayout(UserWizard(on_success=self.on_success1, old_user=user))
        self.on_successful = on_successful

    def on_success1(self):
        self.on_successful()
        QMessageBox.information(self, 'Congratulations', 'Account was successfully edited!', QMessageBox.Ok)
        self.close()