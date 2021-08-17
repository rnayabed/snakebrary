from window.helpers.user_info_vbox import UserInfoVBox
from window.dashboard.edit_user import EditUser
from window.dashboard.book_wizard_window import BookWizardWindow
from window.dashboard.book_holders_window import BookHoldersWindow
from logic.user import User, UserPrivilege
from logic.database import Database
from os import name, stat
from window.helpers.helpers import center_screen, delete_layouts_in_layout, get_font_size
from window.helpers.enhanced_controls import ImageView
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from logic.book import Book, BookHolder
from PySide6.QtWidgets import (QAbstractScrollArea, QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools


class UserInfo(QDialog):

    def __init__(self, user: User, current_user: User, dashboard_on_user_edited=None, parent=None):
        super(UserInfo, self).__init__(parent)
        
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle("User Information")
        self.setFixedHeight(320)

        self.user_info_vbox = UserInfoVBox(user, current_user, dashboard_on_user_edited, self)
        self.setLayout(self.user_info_vbox)

    
    