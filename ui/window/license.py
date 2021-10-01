from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QPlainTextEdit, QPushButton, QVBoxLayout


class License(QDialog):

    def __init__(self, parent):
        super(License, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle('SnakeBrary - License')
        self.resize(450,500)

        layout = QVBoxLayout()

        license_plain_text_edit = QPlainTextEdit()
        license_plain_text_edit.setReadOnly(True)
        license_plain_text_edit.setPlainText(open('LICENSE').read())

        layout.addWidget(license_plain_text_edit)

        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

        layout.addWidget(close_button)

        self.setLayout(layout)
