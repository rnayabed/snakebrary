from window.connection_details_widget import ConnectionDetailsWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

from logic.database import Database
from logic.user import UserPrivilege
from window.dashboard.dashboard import Dashboard
from window.helpers.enhanced_controls import LineEdit
from window.helpers.helpers import get_font_size, center_screen


class LoginPrompt(QWidget):

    def __init__(self, parent=None):
        super(LoginPrompt, self).__init__(parent)

        self.setWindowTitle('Snakebrary')
        self.setFixedSize(400, 420)

        heading = QLabel('Sign in')
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(get_font_size(30))

        sub_heading = QLabel('to continue to Snakebrary')
        sub_heading.setAlignment(Qt.AlignCenter)
        sub_heading.setFont(get_font_size(15))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(sub_heading)

        self.username_field = LineEdit('Username')
        self.password_field = LineEdit('Password', password_mode=True)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.on_login_button_click)

        self.forgot_password_button = QPushButton('Forgot Password')
        self.forgot_password_button.clicked.connect(self.on_forgot_password_button_click)
        self.forgot_password_button.setProperty('class', 'danger')

        self.sql_server_settings_button = QPushButton('MySQL Settings')
        self.sql_server_settings_button.clicked.connect(self.sql_server_settings_button_clicked)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)

        # Create layout and add widgets
        layout.addLayout(self.username_field)
        layout.addLayout(self.password_field)
        layout.addWidget(self.error_label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.forgot_password_button)
        layout.addWidget(self.sql_server_settings_button)

        layout.setSpacing(10)

        # Set dialog layout
        self.setLayout(layout)
    
    def sql_server_settings_button_clicked(self):
        Database.close_connection()
        self.connection_details = ConnectionDetailsWidget(self.on_connection_configure_success)
        self.connection_details.show()
        center_screen(self.connection_details)
        self.close()

    def on_connection_configure_success(self):
        self.login_prompt = LoginPrompt()
        self.login_prompt.show()
        center_screen(self.login_prompt)
        

    def on_login_button_click(self):
        try_username = self.username_field.line_edit.text()
        try_password = self.password_field.line_edit.text()

        users = Database.get_users_by_username(try_username)

        print ('Users', users)

        if len(users) == 0:
            self.set_error("Invalid username/password")
            return

        if users[0].password != try_password:
            self.set_error("Invalid username/password")
            return

        self.set_error(None)
        self.disable_prompt(True)

        self.dash = Dashboard(users[0])
        self.dash.show()
        center_screen(self.dash)
        self.close()

    def on_forgot_password_button_click(self):
        try_username = self.username_field.line_edit.text()

        if len(try_username) == 0:
            msg_text = 'No username was provided.'
        else:
            users = Database.get_users_by_username(try_username)

            if len(users) == 0:
                msg_text = 'No user with the provided username was found. Contact administrator.'
            else:
                hint = users[0].password_hint

                if hint == '':
                    msg_text = 'Your account has no password hint.'
                else:
                    msg_text = f'Your password hint is:\n{hint}\n'

                if users[0].privilege == UserPrivilege.NORMAL:
                    msg_text += '\nContact administrator(s) for further help.'
                elif users[0].privilege == UserPrivilege.ADMIN:
                    msg_text += '\nContact master administrator for further help.'
                else:
                    msg_text += '\nThis account cannot be recovered if password is forgotten.'

        QMessageBox.warning(self, 'Warning', msg_text, QMessageBox.Ok)

    def set_error(self, error):
        self.error_label.setText(error)

    def disable_prompt(self, disable):
        self.username_field.line_edit.setReadOnly(disable)
        self.password_field.line_edit.setReadOnly(disable)
        self.login_button.setDisabled(disable)
        self.forgot_password_button.setDisabled(disable)
