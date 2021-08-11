from PySide6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QMessageBox)

from PySide6.QtCore import Qt

from window.helpers.helpers import get_font_size, center_screen
from window.helpers.new_user_layout import NewUserLayout

from logic.user import UserPrivilege
from window.login_prompt import LoginPrompt


class Welcome(QWidget):

    def __init__(self, app):
        super(Welcome, self).__init__(None)

        self.app = app

        self.setWindowTitle('Welcome')
        self.setFixedSize(500, 650)

        heading = QLabel('Welcome to snakebrary!')
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(get_font_size(30))

        sub_heading_1 = QLabel('<i>A Sweet and Simple Library Management System</i>')
        sub_heading_1.setAlignment(Qt.AlignCenter)
        sub_heading_1.setFont(get_font_size(13))
        sub_heading_1.setStyleSheet('padding-bottom: 30')

        sub_heading_2 = QLabel('Fill the form below to get started!')
        sub_heading_2.setAlignment(Qt.AlignCenter)
        sub_heading_2.setFont(get_font_size(15))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(sub_heading_1)
        layout.addWidget(sub_heading_2)

        master_user_layout = NewUserLayout(on_success=self.on_success, user_privilege=UserPrivilege.MASTER)

        layout.addLayout(master_user_layout)

        layout.setSpacing(10)

        self.setLayout(layout)

        self.login_prompt = LoginPrompt(self.app)

    def on_success(self):
        QMessageBox.information(self, 'Congratulations', 'Snakebrary is now all set. You may now login as your master '
                                                         'account and start adding books, create new administrators, '
                                                         'users, etc.',
                                QMessageBox.Ok)

        self.login_prompt.show()
        center_screen(self.login_prompt)
        self.close()
