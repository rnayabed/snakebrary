from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QMessageBox
from logic.user import UserPrivilege
from ui.layouts_and_widgets.user_wizard import UserWizard


class AddUser(QDialog):

    def __init__(self, new_user_privilege:UserPrivilege, on_successful, parent=None):
        super(AddUser, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)
        
        if new_user_privilege == UserPrivilege.ADMIN:
            prefix_label = 'Administrator'
        else:
            prefix_label = 'User'

        self.setWindowTitle(f'Add New {prefix_label}')
        self.resize(800, 600)

        self.setLayout(UserWizard(on_success=self.on_success1, new_user_privilege=new_user_privilege))
        self.on_successful = on_successful

    def on_success1(self):
        self.on_successful()
        QMessageBox.information(self, 'Congratulations', 'Account was successfully added!', QMessageBox.Ok)
        self.close()