from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QPushButton

from logic.database import Database
from window.helpers.enhanced_controls import FilePicker, ImageView, LineEdit
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

        self.new_user_photo_path_field = FilePicker('Profile picture (Optional)', on_select=self.on_user_photo_selected, on_clear=self.on_user_photo_cleared)

        self.new_user_photo_preview = ImageView('Preview', 100, 100)

        self.photo_hbox = QHBoxLayout()
        self.photo_hbox.addLayout(self.new_user_photo_path_field)
        self.photo_hbox.addWidget(self.new_user_photo_preview)

        self.new_user_name_field = LineEdit(f'{prefix_label} Name')

        self.new_user_username_field = LineEdit(f'{prefix_label} Username')
        self.new_user_password_field = LineEdit(f'{prefix_label} Password', password_mode=True)
        self.new_user_password_field_confirm = LineEdit(f'Confirm {prefix_label} Password', password_mode=True)
        self.new_user_password_field_hint = LineEdit(f'Password Hint (Optional)')

        self.proceed_button = QPushButton('Proceed')
        self.proceed_button.clicked.connect(self.on_proceed_button_clicked)

        # Create layout and add widgets
        self.addLayout(self.photo_hbox)
        self.addLayout(self.new_user_name_field)
        self.addLayout(self.new_user_username_field)
        self.addLayout(self.new_user_password_field)
        self.addLayout(self.new_user_password_field_confirm)
        self.addLayout(self.new_user_password_field_hint)
        self.addWidget(self.proceed_button)
    
    def on_user_photo_selected(self, img_path):
        self.new_user_photo_preview.set_image_from_path(img_path)
            
    def on_user_photo_cleared(self):
        self.new_user_photo_path_field.line_edit.clear()
        self.new_user_photo_preview.clear_image()

    def on_proceed_button_clicked(self):
        proposed_new_user_photo_path = self.new_user_photo_path_field.line_edit.text()
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

        if Database.is_new_setup():
            Database.create_new_tables()

        old_users = Database.get_users_by_username(proposed_new_user_username)
        if len(old_users) > 0:
            QMessageBox.critical(None, 'Error', f'''User with same username already exists.
Name: {old_users[0].name}
Privilege: {UserPrivilege.get_ui_name(old_users[0].privilege)}
Date Time Created: {old_users[0].date_time_created}''', QMessageBox.Ok)
            return
        
        new_user = User(proposed_new_user_username, proposed_new_user_password,
                                 proposed_new_user_password_hint, proposed_new_user_name,
                                 privilege=self.user_privilege)
            
        if proposed_new_user_photo_path != '':
            file = open(proposed_new_user_photo_path, 'rb')
            new_user.photo = file.read()
            file.close()

        new_user.print_details()

        Database.create_new_user(new_user)
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
