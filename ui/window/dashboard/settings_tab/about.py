import importlib.metadata
import platform
from sqlite3.dbapi2 import sqlite_version
from ui.window.license import License
from ui.helpers.enhanced_controls import ImageView

from PySide6 import QtCore
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QLabel

from ui.helpers.helpers import get_label_style_sheet_font_size
from constants import Constants


class About(QWidget):

    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        app_icon_hbox = QHBoxLayout()
        app_icon = ImageView('App Icon', 150, 150, style=None)
        app_icon.set_image_from_path('assets/app_icon.png')
        app_icon_hbox.addWidget(app_icon)
        layout.addLayout(app_icon_hbox)

        heading_label = QLabel('SnakeBrary')
        heading_label.setStyleSheet(get_label_style_sheet_font_size(25))
        heading_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(heading_label)

        sub_heading_label = QLabel('<i>A Sweet and Simple Library Management System</i>')
        sub_heading_label.setStyleSheet(get_label_style_sheet_font_size(17))
        sub_heading_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(sub_heading_label)

        maker_label = QLabel('Made by Debayan Sutradhar')
        maker_label.setStyleSheet(get_label_style_sheet_font_size(15))
        maker_label.setAlignment(QtCore.Qt.AlignCenter)
        maker_label.setContentsMargins(QtCore.QMargins(0, 0, 0, 30))
        layout.addWidget(maker_label)

        source_code_hyperlink = QLabel(f'<a href="{Constants.GITHUB_URL}">Source Code</a>')
        source_code_hyperlink.setOpenExternalLinks(True)
        source_code_hyperlink.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(source_code_hyperlink)

        license_button = QPushButton('License')
        license_button.setMinimumWidth(5)
        license_button.clicked.connect(self.license_button_clicked)
        license_button.setContentsMargins(QtCore.QMargins(0, 0, 0, 30))
        layout.addWidget(license_button)

        version_info_hbox = QHBoxLayout()
        version_info_hbox.setAlignment(QtCore.Qt.AlignCenter)

        version_info_hbox.addWidget(QLabel(f'Version {Constants.VERSION}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'Python {platform.python_version()}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'SQLite {sqlite_version}'))
        version_info_hbox.addWidget(self.get_separator())

        version_info_hbox.addWidget(QLabel(f'Qt {QtCore.qVersion()}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'PySide6 {self.get_module_version("PySide6")}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'MySQL Connector {self.get_module_version("mysql-connector-python")}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'qt-material {self.get_module_version("qt-material")}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'qtawesome {self.get_module_version("qtawesome")}'))
        version_info_hbox.addWidget(self.get_separator())
        version_info_hbox.addWidget(QLabel(f'{platform.system()} {platform.release()}'))

        layout.addLayout(version_info_hbox)

        self.setLayout(layout)

    @staticmethod
    def get_module_version(module):
        return importlib.metadata.version(module)

    @staticmethod
    def get_separator():
        separator_label = QLabel('|')
        separator_label.setStyleSheet('color: grey;')
        return separator_label

    def license_button_clicked(self):
        license_window = License(self)
        license_window.exec()
