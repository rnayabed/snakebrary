from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QSizePolicy
from PySide6.QtCore import QSize


class AdminBooksTab(QWidget):

    def __init__(self, current_user, parent=None):
        super(AdminBooksTab, self).__init__(parent)

        self.current_user = current_user

        layout = QVBoxLayout()

        grid = QGridLayout()

        self.manage_users_button = QPushButton('Manage users')
        grid.addWidget(self.manage_users_button, 0, 0)

        self.manage_books_button = QPushButton('Manage books')
        grid.addWidget(self.manage_books_button, 0, 1)

        grid.setRowMinimumHeight(0, 300)
        layout.addLayout(grid)

        self.setLayout(layout)


