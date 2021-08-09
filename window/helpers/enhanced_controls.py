from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt


class LineEdit(QVBoxLayout):

    def __init__(self, info, init_value=None, password_mode=False):
        super(LineEdit, self).__init__()

        self.info_label = QLabel(info)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        self.error_label.setAlignment(Qt.AlignRight)

        self.upper = QHBoxLayout()
        self.upper.addWidget(self.info_label)
        self.upper.addWidget(self.error_label)

        self.line_edit = QLineEdit()

        if password_mode:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.line_edit.setText(init_value)

        self.setSpacing(3)
        self.addLayout(self.upper)
        self.addWidget(self.line_edit)

    def on_error(self, error):
        self.error_label.setText(error)

    def on_success(self):
        self.error_label.clear()


class ComboBox(QHBoxLayout):

    def __init__(self, info, l):
        super(ComboBox, self).__init__()

        self.label = QLabel(info)

        self.combo_box = QComboBox()
        self.combo_box.addItems(l)

        self.addWidget(self.label)
        self.addWidget(self.combo_box)