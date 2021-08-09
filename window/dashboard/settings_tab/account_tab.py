
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AccountTab(QWidget):

    def __init__(self, parent=None):
        super(AccountTab, self).__init__(parent)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Coming soon"))

        self.setLayout(layout)

