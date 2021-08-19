from sqlite3.dbapi2 import sqlite_version
import importlib.metadata
from PySide6 import QtCore
import platform
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel

from ui.helpers.helpers import get_font_size


class About(QWidget):

    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        github_url = 'https://github.com/rnayabed/SnakeBrary'
        license_url = 'https://github.com/rnayabed/SnakeBrary/blob/master/LICENSE'
        synopsis_url = 'https://raw.githubusercontent.com/rnayabed/SnakeBrary/master/synopsis.docx'
        version = '1.0.0'

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        heading_label = QLabel('SnakeBrary')
        heading_label.setFont(get_font_size(25))
        heading_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(heading_label)
        
        sub_heading_label = QLabel('<i>A Sweet and Simple Library Management System</i>')
        sub_heading_label.setFont(get_font_size(17))
        sub_heading_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(sub_heading_label)

        maker_label = QLabel('Made by Debayan Sutradhar, 12 M')
        maker_label.setFont(get_font_size(15))
        maker_label.setAlignment(QtCore.Qt.AlignCenter)
        maker_label.setContentsMargins(QtCore.QMargins(0,0,0,30))
        layout.addWidget(maker_label)

        school_label = QLabel('DPS Ruby Park, Kolkata')
        school_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(school_label)

        small_info_label = QLabel('CBSE Class 12 Computer Science project assignment')
        small_info_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(small_info_label)

        synopsis_label = QLabel(f'<a href="{synopsis_url}">Project Synopsis</a>')
        synopsis_label.setOpenExternalLinks(True)
        synopsis_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(synopsis_label)

        source_code_hyperlink = QLabel(f'<a href="{github_url}">Source Code</a>')
        source_code_hyperlink.setOpenExternalLinks(True)
        source_code_hyperlink.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(source_code_hyperlink)

        license_label = QLabel(f'This software is <b>Free</b> and <b>Open Source</b> and is licensed under the <a href="{license_url}">GNU GPLv3</a> license.')
        license_label.setOpenExternalLinks(True)
        license_label.setAlignment(QtCore.Qt.AlignCenter)
        license_label.setContentsMargins(QtCore.QMargins(0, 0, 0, 30))
        layout.addWidget(license_label)

        
        version_info_hbox = QHBoxLayout()
        version_info_hbox.setAlignment(QtCore.Qt.AlignCenter)

        version_info_hbox.addWidget(QLabel(f'Version {version}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'Qt {QtCore.qVersion()}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'Python {platform.python_version()}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'SQLite {sqlite_version}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'MySQL Connector {importlib.metadata.version("mysql-connector-python")}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'qt-material {importlib.metadata.version("qt-material")}'))
        version_info_hbox.addWidget(self.get_seperator())
        version_info_hbox.addWidget(QLabel(f'{platform.system()} {platform.release()}'))

        layout.addLayout(version_info_hbox)

        self.setLayout(layout)
    
    def get_seperator(self):
        seperator_label = QLabel('|')
        seperator_label.setStyleSheet('color: grey;')
        return seperator_label

