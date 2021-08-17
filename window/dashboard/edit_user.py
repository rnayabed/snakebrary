from PySide6 import QtCore
from window.helpers.user_wizard import UserWizard
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QWidget, QLabel, QMessageBox)

from PySide6.QtCore import Qt

from window.helpers.helpers import get_font_size, center_screen

from logic.user import UserPrivilege


class EditUser(QDialog):

    def __init__(self, user, on_successful, parent=None):
        super(EditUser, self).__init__(parent)
        
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle('Edit User')
        self.resize(800, 600)

        self.setLayout(UserWizard(on_success=self.on_success1, old_user=user))
        self.on_successful = on_successful

    def on_success1(self):
        self.on_successful()
        QMessageBox.information(self, 'Congratulations', 'Account was successfully edited!', QMessageBox.Ok)
        self.close()