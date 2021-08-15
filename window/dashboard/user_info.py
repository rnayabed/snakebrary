from window.dashboard.edit_user import EditUser
from window.dashboard.book_wizard_window import BookWizardWindow
from window.dashboard.book_holders_window import BookHoldersWindow
from window.dashboard.book_ratings_layout import BookRatingsLayout
from logic.user import User, UserPrivilege
from logic.database import Database
from os import name, stat
from window.helpers.helpers import center_screen, delete_layouts_in_layout, get_font_size
from window.helpers.enhanced_controls import ImageView
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from logic.book import Book, BookHolder
from PySide6.QtWidgets import (QAbstractScrollArea, QHBoxLayout, QLabel, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools


class UserInfo(QWidget):

    def __init__(self, user: User, dashboard_on_users_edited, current_user: User, parent=None):
        super(UserInfo, self).__init__(parent)

        self.dashboard_on_users_edited = dashboard_on_users_edited
        self.current_user = current_user
        self.user = user

        self.setWindowTitle("User Information")
        self.resize(800,600)


        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(QtCore.Qt.AlignTop)

        hbox_1 = QHBoxLayout()

        self.profile_photo = ImageView('Profile Photo', 300, 300)
        hbox_1.addWidget(self.profile_photo)

        self.name_label = QLabel()

        self.username_label = QLabel()

        self.password_widget = PasswordWidget(self.user)

        self.privilege_label = QLabel()

        self.book_history_button = QPushButton('Show Book history')

        self.edit_user_button = QPushButton('Edit')
        self.edit_user_button.clicked.connect(self.edit_user_button_onclick)

        self.delete_user_button = QPushButton('Delete')
        self.delete_user_button.setProperty('class', 'danger')
        self.delete_user_button.clicked.connect(self.delete_user_button_onclick)

        self.edit_delete_button_hbox = QHBoxLayout()
        self.edit_delete_button_hbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
        self.edit_delete_button_hbox.addWidget(self.edit_user_button)
        self.edit_delete_button_hbox.addWidget(self.delete_user_button)

        self.edit_delete_button_widget = QWidget()
        self.edit_delete_button_widget.setContentsMargins(QtCore.QMargins(0,0,0,0))
        self.edit_delete_button_widget.setLayout(self.edit_delete_button_hbox)


        vbox_labels_1 = QVBoxLayout()
        vbox_labels_1.setAlignment(QtCore.Qt.AlignTop)
        vbox_labels_1.addWidget(self.name_label)
        vbox_labels_1.addWidget(self.username_label)
        vbox_labels_1.addWidget(self.privilege_label)
        vbox_labels_1.addWidget(self.password_widget)
        vbox_labels_1.addWidget(self.book_history_button)
        vbox_labels_1.addWidget(self.edit_delete_button_widget)

        hbox_1.addLayout(vbox_labels_1)


        main_vbox.addLayout(hbox_1)

        self.setLayout(main_vbox)

        self.configure_ui()
    
    def configure_ui(self):
        if self.user.photo == None:
            self.profile_photo.clear_image()
            self.profile_photo.hide()
        else:
            self.profile_photo.set_image_from_blob(self.user.photo)
            self.profile_photo.show()
        

        self.name_label.setText(f'Name: {self.user.name}')
        self.username_label.setText(f'Username: {self.user.username}')
        self.privilege_label.setText(f'Privilege: {UserPrivilege.get_ui_name(self.user.privilege)}')

        if (self.current_user.privilege == UserPrivilege.ADMIN and self.user.privilege == UserPrivilege.MASTER) or (self.current_user.privilege == self.user.privilege and self.current_user.username != self.user.username and self.current_user.privilege == UserPrivilege.ADMIN):
            self.password_widget.hide()
            self.edit_delete_button_widget.hide()
            self.edit_delete_button_widget.hide()
        
        if self.current_user.username == self.user.username:
            self.delete_user_button.hide()

    def delete_user_button_onclick(self):
        warning_box = QMessageBox.warning(self, 'Warning', f'''Are you sure you want to delete the following user
Name: {self.user.name}
Username: {self.user.username}''', QMessageBox.Yes, QMessageBox.No)

        if warning_box == QMessageBox.Yes:
            Database.delete_user(self.user.username)
            self.dashboard_on_users_edited()
            self.close()
    
    def edit_user_button_onclick(self):
        self.edit_user_window = EditUser(self.user, self.on_user_edited)
        self.edit_user_window.show()
        center_screen(self.edit_user_window)
    
    def on_user_edited(self):
        self.dashboard_on_users_edited()
        self.user = Database.get_users_by_username(self.user.username)[0]
        self.configure_ui()

class PasswordWidgetMode:

    HIDE = 0,
    SHOW = 1

class PasswordWidget(QWidget):

    def __init__(self, user):
        super(PasswordWidget, self).__init__(None)

        self.user = user

        self.password_label = QLabel()
        self.password_hint_label = QLabel()
        self.password_show_hide_button = QPushButton()
        self.password_show_hide_button.clicked.connect(self.toggle_mode)

        password_vbox = QVBoxLayout()
        password_vbox.setContentsMargins(QtCore.QMargins(0,0,0,0))
        password_vbox.addWidget(self.password_label)
        password_vbox.addWidget(self.password_hint_label)
        password_vbox.addWidget(self.password_show_hide_button)

        self.setLayout(password_vbox)

        self.set_current_mode(PasswordWidgetMode.HIDE)
    
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
        