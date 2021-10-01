from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QGraphicsColorizeEffect, QWidget, QVBoxLayout, QLabel, QPushButton, \
    QMessageBox

from logic.database import Database
from logic.user import UserPrivilege
from ui.helpers.enhanced_controls import LineEdit
from ui.helpers.helpers import get_font_size, center_screen
from ui.window.connection_details_widget import ConnectionDetailsWidget
from ui.window.dashboard.dashboard import Dashboard



class LoginPrompt(QWidget):

    def __init__(self, parent=None):
        super(LoginPrompt, self).__init__(parent)

        self.setWindowTitle('SnakeBrary')
        self.setFixedSize(400, 420)

        heading = QLabel('Sign in')
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(get_font_size(30))

        sub_heading = QLabel('to continue to SnakeBrary')
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
        self.error_label.setAlignment(Qt.AlignCenter)

        # Create layout and add widgets
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_field)
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
        self.disable_prompt(True)

        self.username_field.on_success()

        try_username = self.username_field.line_edit.text()
        try_password = self.password_field.line_edit.text()

        user = Database.get_user_by_username(try_username)

        if user == None:
            self.set_error("Invalid username/password")
            self.disable_prompt(False)
            return

        if user.password != try_password:
            self.set_error("Invalid username/password")
            self.disable_prompt(False)
            return
        
        if user.is_disabled:
            self.set_error('Account disabled. Contact administrator.')
            self.disable_prompt(False)
            return

        
        self.set_success('Successfully Logged in!')
        self.dash = Dashboard(user)
        self.dash.show()
        center_screen(self.dash)
        self.close()

    def on_forgot_password_button_click(self):
        try_username = self.username_field.line_edit.text()

        if len(try_username) < 1:
            self.username_field.on_error('Empty username!')
            return

        self.username_field.on_success()

        user = Database.get_user_by_username(try_username)

        if user == None:
            msg_text = 'No user with the provided username was found. Contact administrator.'
        else:
            hint = user.password_hint

            if hint == '':
                msg_text = 'Your account has no password hint.'
            else:
                msg_text = f'Your password hint is:\n{hint}\n'

            if user.privilege == UserPrivilege.NORMAL:
                msg_text += '\nContact administrator for further help.'
            elif user.privilege == UserPrivilege.ADMIN:
                msg_text += '\nContact master administrator for further help.'
            else:
                msg_text += '\nThis account cannot be recovered if password is forgotten.'

        QMessageBox.warning(self, 'Warning', msg_text, QMessageBox.Ok)

    def set_error(self, error):
        self.error_label.setText(error)
        self.error_label.setStyleSheet("color: red;")
        QApplication.instance().processEvents()
    
    def set_success(self, error):
        self.error_label.setText(error)
        self.error_label.setStyleSheet("color: green;")
        QApplication.instance().processEvents()

    def disable_prompt(self, disable):
        self.username_field.line_edit.setReadOnly(disable)
        self.password_field.line_edit.setReadOnly(disable)
        self.login_button.setDisabled(disable)
        self.forgot_password_button.setDisabled(disable)
        QApplication.instance().processEvents()
