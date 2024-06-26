from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QCheckBox

from logic.database import Database
from ui.helpers.enhanced_controls import LineEdit
from ui.helpers.helpers import get_label_style_sheet_font_size


class ConnectionDetailsWidget(QWidget):

    def __init__(self, on_success=None, parent=None):
        super(ConnectionDetailsWidget, self).__init__(parent)

        self.holder_value_to_prevent_reference_loss = None
        self.setWindowTitle('SnakeBrary')
        self.on_success = on_success
        self.setFixedSize(420, 480)

        layout = QVBoxLayout()

        heading = QLabel('Connect to MySQL Server')
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet(get_label_style_sheet_font_size(20))
        layout.addWidget(heading)

        sub_heading = QLabel('to use SnakeBrary')
        sub_heading.setAlignment(Qt.AlignCenter)
        sub_heading.setStyleSheet(get_label_style_sheet_font_size(15))
        layout.addWidget(sub_heading)

        self.host_field = LineEdit('Host')
        self.port_field = LineEdit('Port')
        self.user_field = LineEdit('User')
        self.password_field = LineEdit('Password', password_mode=True)

        self.remember_me_checkbox = QCheckBox('Remember Connection Settings')
        self.remember_me_checkbox.setChecked(True)

        self.connect_server_button = QPushButton('Connect')
        self.connect_server_button.clicked.connect(self.connect_server_button_clicked)

        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)

        # Create layout and add widgets
        layout.addWidget(self.host_field)
        layout.addWidget(self.port_field)
        layout.addWidget(self.user_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.remember_me_checkbox)
        layout.addWidget(self.error_label)
        layout.addWidget(self.connect_server_button)

        layout.setSpacing(10)

        # Set dialog layout
        self.setLayout(layout)

        self.get_local_saved_settings()

    def get_local_saved_settings(self):
        self.host_field.line_edit.setText(Database.get_local_database_server_host())
        self.user_field.line_edit.setText(Database.get_local_database_server_user())
        self.port_field.line_edit.setText(Database.get_local_database_server_port())
        self.password_field.line_edit.setText(Database.get_local_database_server_password())

    def connect_server_button_clicked(self):

        self.disable_prompt(True)

        host = self.host_field.line_edit.text()
        port = self.port_field.line_edit.text()
        user = self.user_field.line_edit.text()
        password = self.password_field.line_edit.text()

        error = False

        if len(host) < 1:
            self.host_field.on_error('Invalid host')
            error = True
        else:
            self.host_field.on_success()

        if not port.isnumeric():
            self.port_field.on_error('Invalid port')
            error = True
        else:
            self.port_field.on_success()

        if error:
            self.error_label.setText('')
            self.disable_prompt(False)
            return

        QApplication.instance().processEvents()

        try:
            Database.create_connection(host, user, password, port)

            if Database.is_new_local_setup():
                Database.create_local_database_settings_table()

            if self.remember_me_checkbox.isChecked():
                Database.set_local_connection_settings(host, port, user, password)
            else:
                Database.clear_local_connection_settings()

            Database.save_local_database()

            self.error_label.setText('')

            if self.on_success is not None:
                self.holder_value_to_prevent_reference_loss = self.on_success()

            self.close()
        except Exception as e:
            self.error_label.setText(str(e))

        self.disable_prompt(False)

    def disable_prompt(self, status):
        self.host_field.line_edit.setReadOnly(status)
        self.port_field.line_edit.setReadOnly(status)
        self.user_field.line_edit.setReadOnly(status)
        self.password_field.line_edit.setReadOnly(status)
        self.connect_server_button.setDisabled(status)
        QApplication.instance().processEvents()
