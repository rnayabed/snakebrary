from enum import Enum

from PySide6 import QtCore
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from logic.database import Database
from logic.user import User, UserPrivilege
from ui.helpers.enhanced_controls import ImageView
from ui.helpers.helpers import get_label_style_sheet_font_size, center_screen
from ui.window.edit_user import EditUser


class UserInfoVBox(QVBoxLayout):

    def __init__(self, user: User, current_user: User, dashboard_on_user_edited, parent, is_account_tab=False,
                 disable_edit_options=False):
        super(UserInfoVBox, self).__init__(parent)

        self.edit_user_window = None
        self.dashboard_on_user_edited = dashboard_on_user_edited
        self.current_user = current_user
        self.parent = parent
        self.user = user
        self.is_account_tab = is_account_tab
        self.disable_edit_options = disable_edit_options

        self.setAlignment(QtCore.Qt.AlignTop)

        hbox_1 = QHBoxLayout()

        self.profile_photo = ImageView('Profile Photo', 300, 300)
        hbox_1.addWidget(self.profile_photo)

        self.name_label = QLabel()
        self.name_label.setStyleSheet(get_label_style_sheet_font_size(30))

        self.username_label = QLabel()

        self.password_widget = PasswordWidget(self.user)

        self.privilege_label = QLabel()

        self.date_time_created_label = QLabel()

        self.edit_user_button = QPushButton('Edit')
        self.edit_user_button.clicked.connect(self.edit_user_button_onclick)

        self.delete_user_button = QPushButton('Delete')
        self.delete_user_button.setProperty('class', 'danger')
        self.delete_user_button.clicked.connect(self.delete_user_button_onclick)

        self.edit_delete_button_hbox = QHBoxLayout()
        self.edit_delete_button_hbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.edit_delete_button_hbox.addWidget(self.edit_user_button)
        self.edit_delete_button_hbox.addWidget(self.delete_user_button)

        self.disable_enable_button = QPushButton()

        self.edit_delete_button_widget = QWidget()
        self.edit_delete_button_widget.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.edit_delete_button_widget.setLayout(self.edit_delete_button_hbox)

        vbox_labels_1 = QVBoxLayout()
        vbox_labels_1.setAlignment(QtCore.Qt.AlignTop)
        vbox_labels_1.addWidget(self.name_label)
        vbox_labels_1.addWidget(self.username_label)
        vbox_labels_1.addWidget(self.privilege_label)
        vbox_labels_1.addWidget(self.date_time_created_label)
        vbox_labels_1.addWidget(self.password_widget)
        vbox_labels_1.addWidget(self.disable_enable_button)
        vbox_labels_1.addWidget(self.edit_delete_button_widget)

        hbox_1.addLayout(vbox_labels_1)

        self.addLayout(hbox_1)

        self.configure_ui()

    def configure_ui(self):
        self.password_widget.reload_user(self.user)

        if self.user.photo is None:
            self.profile_photo.clear_image()
            self.profile_photo.hide()
        else:
            self.profile_photo.set_image_from_blob(self.user.photo)
            self.profile_photo.show()

        self.name_label.setText(self.user.name)
        self.username_label.setText(f'Username: {self.user.username}')
        self.privilege_label.setText(f'Privilege: {UserPrivilege.get_ui_name(self.user.privilege)}')
        self.date_time_created_label.setText(f'Date/Time created: {self.user.date_time_created}')

        is_enable_disable_button_visible = True

        if (self.current_user.privilege == UserPrivilege.ADMIN and self.user.privilege == UserPrivilege.MASTER) or (
                self.current_user.privilege == self.user.privilege and
                self.current_user.username != self.user.username and
                self.current_user.privilege == UserPrivilege.ADMIN
        ):
            self.password_widget.hide()
            self.edit_delete_button_widget.hide()
            self.disable_enable_button.hide()
            is_enable_disable_button_visible = False

        if self.current_user.privilege == UserPrivilege.NORMAL:
            self.password_widget.hide()
            self.disable_enable_button.hide()
            is_enable_disable_button_visible = False

        if self.is_account_tab:
            self.password_widget.hide()
            self.privilege_label.hide()

        if self.current_user.username == self.user.username:
            self.delete_user_button.hide()
            self.disable_enable_button.hide()
            is_enable_disable_button_visible = False

        if self.disable_edit_options:
            self.delete_user_button.hide()
            self.edit_delete_button_widget.hide()
            self.password_widget.hide()
            self.disable_enable_button.hide()
            is_enable_disable_button_visible = False

        if is_enable_disable_button_visible:
            self.configure_disable_enable_button()

    def configure_disable_enable_button(self):
        self.disconnect_slots_disable_enable_button()

        if self.user.is_disabled:
            self.disable_enable_button.show()
            self.disable_enable_button.setText('Enable')
            self.disable_enable_button.clicked.connect(lambda: self.enable_disable_user(False))
        else:
            self.disable_enable_button.show()
            self.disable_enable_button.setText('Disable')
            self.disable_enable_button.clicked.connect(lambda: self.enable_disable_user(True))

    def enable_disable_user(self, is_disabled):
        self.user.is_disabled = is_disabled
        Database.update_user(self.user)

        self.configure_disable_enable_button()

    def disconnect_slots_disable_enable_button(self):
        try:
            self.disable_enable_button.clicked.disconnect()
        except:
            pass

    def delete_user_button_onclick(self):
        warning_box = QMessageBox.warning(self.parent, 'Warning', f'''Are you sure you want to delete the following user
Name: {self.user.name}
Username: {self.user.username}''', QMessageBox.Yes, QMessageBox.No)

        if warning_box == QMessageBox.Yes:
            Database.delete_user(self.user.username)
            if self.dashboard_on_user_edited is not None:
                self.dashboard_on_user_edited()
            self.parent.close()

    def edit_user_button_onclick(self):
        self.edit_user_window = EditUser(self.user, self.on_user_edited, self.parent)
        self.edit_user_window.exec()
        center_screen(self.edit_user_window)

    def on_user_edited(self):
        if self.dashboard_on_user_edited is not None:
            self.dashboard_on_user_edited()
        self.user = Database.get_user_by_username(self.user.username)
        self.configure_ui()
        center_screen(self.parent)


class PasswordWidgetMode(Enum):
    HIDE = 0,
    SHOW = 1


class PasswordWidget(QWidget):

    def __init__(self, user):
        super(PasswordWidget, self).__init__(None)

        self.mode = None
        self.user = user

        self.password_label = QLabel()
        self.password_hint_label = QLabel()
        self.password_show_hide_button = QPushButton()
        self.password_show_hide_button.clicked.connect(self.toggle_mode)

        password_vbox = QVBoxLayout()
        password_vbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        password_vbox.addWidget(self.password_label)
        password_vbox.addWidget(self.password_hint_label)
        password_vbox.addWidget(self.password_show_hide_button)

        self.setLayout(password_vbox)

        self.set_current_mode(PasswordWidgetMode.HIDE)

    def reload_user(self, user):
        self.user = user
        self.set_current_mode(self.mode)

    def set_current_mode(self, mode: PasswordWidgetMode):
        self.mode = mode
        if self.mode == PasswordWidgetMode.HIDE:
            self.password_label.setText('Password: ********')
            self.password_hint_label.setText('Password Hint: *******')
            self.password_show_hide_button.setText('Show Password and Hint')
        elif self.mode == PasswordWidgetMode.SHOW:
            self.password_label.setText(f'Password : {self.user.password}')

            if self.user.password_hint == '':
                self.password_hint_label.setText('Password Hint not configured')
            else:
                self.password_hint_label.setText(f'Password Hint: {self.user.password_hint}')

            self.password_show_hide_button.setText('Hide Password and Hint')

    def toggle_mode(self):
        if self.mode == PasswordWidgetMode.HIDE:
            self.set_current_mode(PasswordWidgetMode.SHOW)
        else:
            self.set_current_mode(PasswordWidgetMode.HIDE)
