from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QMessageBox

from logic.user import UserPrivilege
from ui.helpers.helpers import get_label_style_sheet_font_size, center_screen
from ui.layouts_and_widgets.user_wizard import UserWizard
from ui.window.login_prompt import LoginPrompt


class Welcome(QWidget):

    def __init__(self):
        super(Welcome, self).__init__(None)

        self.setWindowTitle('Welcome')
        self.resize(800, 600)

        heading = QLabel('Welcome to SnakeBrary!')
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet(get_label_style_sheet_font_size(30))

        sub_heading_1 = QLabel('<i>A Sweet and Simple Library Management System</i>')
        sub_heading_1.setAlignment(Qt.AlignCenter)
        sub_heading_1.setStyleSheet(get_label_style_sheet_font_size(13) + 'padding-bottom: 20;')

        sub_heading_2 = QLabel('Fill the form below to create Master account and get started!')
        sub_heading_2.setAlignment(Qt.AlignCenter)
        sub_heading_2.setStyleSheet(get_label_style_sheet_font_size(15))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(sub_heading_1)
        layout.addWidget(sub_heading_2)

        master_user_layout = UserWizard(on_success=self.on_success, new_user_privilege=UserPrivilege.MASTER)

        layout.addLayout(master_user_layout)

        layout.setSpacing(10)

        self.setLayout(layout)

        self.login_prompt = LoginPrompt()

    def on_success(self):
        QMessageBox.information(self, 'Congratulations', 'SnakeBrary is now all set. You may now login as your master '
                                                         'account and start adding books, create new administrators, '
                                                         'users, etc.',
                                QMessageBox.Ok)

        self.login_prompt.show()
        center_screen(self.login_prompt)
        self.close()
