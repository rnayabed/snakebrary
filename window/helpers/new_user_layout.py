from PySide6.QtWidgets import QVBoxLayout, QPushButton

from logic.database import Database
from window.helpers.enhanced_controls import LineEdit
from logic.user import UserPrivilege, User


class NewUserLayout(QVBoxLayout):

    def __init__(self, on_success=None, on_error=None, user_privilege=UserPrivilege.NORMAL):
        super(NewUserLayout, self).__init__()

        self.user_privilege = user_privilege
        self.on_success = on_success
        self.on_error = on_error

        if user_privilege == UserPrivilege.ADMIN:
            prefix_label = 'Administrator'
        elif user_privilege == UserPrivilege.MASTER:
            prefix_label = 'Master'
        else:
            prefix_label = 'User'

        self.new_user_name_field = LineEdit(f'{prefix_label} Name')
        self.new_user_username_field = LineEdit(f'{prefix_label} Username')
        self.new_user_password_field = LineEdit(f'{prefix_label} Password', password_mode=True)
        self.new_user_password_field_confirm = LineEdit(f'Confirm {prefix_label} Password', password_mode=True)
        self.new_user_password_field_hint = LineEdit(f'Password Hint (Optional)')

        self.proceed_button = QPushButton('Proceed')
        self.proceed_button.clicked.connect(self.on_proceed_button_clicked)

        # Create layout and add widgets
        self.addLayout(self.new_user_name_field)
        self.addLayout(self.new_user_username_field)
        self.addLayout(self.new_user_password_field)
        self.addLayout(self.new_user_password_field_confirm)
        self.addLayout(self.new_user_password_field_hint)
        self.addWidget(self.proceed_button)

    def on_proceed_button_clicked(self):
        proposed_new_user_name = self.new_user_name_field.line_edit.text()
        proposed_new_user_username = self.new_user_username_field.line_edit.text()
        proposed_new_user_password = self.new_user_password_field.line_edit.text()
        proposed_new_user_password_confirm = self.new_user_password_field_confirm.line_edit.text()
        proposed_new_user_password_hint = self.new_user_password_field_hint.line_edit.text()

        error = False

        if len(proposed_new_user_name) < 1:
            self.new_user_name_field.on_error('Too short!')
            error = True
        else:
            self.new_user_name_field.on_success()

        if len(proposed_new_user_username) < 1:
            self.new_user_username_field.on_error('Too short!')
            error = True
        else:
            self.new_user_username_field.on_success()

        if len(proposed_new_user_password) < 8:
            self.new_user_password_field.on_error('Too short - Must be at least 8 characters')
            error = True
        else:
            self.new_user_password_field.on_success()

        if proposed_new_user_password_confirm != proposed_new_user_password:
            self.new_user_password_field_confirm.on_error('Passwords do not match')
            error = True
        else:
            self.new_user_password_field_confirm.on_success()

        if error:
            if self.on_error is not None:
                self.on_error()
            return

        self.set_disable(True)

        # Create new Admin user

        new_new_user_user = User(proposed_new_user_username, proposed_new_user_password,
                                 proposed_new_user_password_hint, proposed_new_user_name,
                                 privilege=self.user_privilege)

        new_new_user_user.print_details()

        Database.create_new_user(new_new_user_user)
        Database.print_all_users()

        if self.on_success is not None:
            self.on_success()

    def set_disable(self, disable):
        self.proceed_button.setDisabled(disable)
        self.new_user_name_field.line_edit.setReadOnly(disable)
        self.new_user_username_field.line_edit.setReadOnly(disable)
        self.new_user_password_field.line_edit.setReadOnly(disable)
        self.new_user_password_field_confirm.line_edit.setReadOnly(disable)
        self.new_user_password_field_hint.line_edit.setReadOnly(disable)
