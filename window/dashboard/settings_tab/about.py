
from window.helpers.helpers import get_font_size
from PySide6 import QtCore
import platform
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class About(QWidget):

    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        github_url = 'https://github.com/rnayabed/SnakeBrary'
        license_url = 'https://github.com/rnayabed/SnakeBrary/blob/master/LICENSE'
        synopsis_url = 'https://raw.githubusercontent.com/rnayabed/SnakeBrary/master/synopsis.docx'
        version = '1.0.0'

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        maker_label = QLabel('Made by Debayan Sutradhar (rnayabed)')
        maker_label.setFont(get_font_size(17))
        layout.addWidget(maker_label)

        layout.addWidget(QLabel('This software was written as CBSE Class 12 Computer Science project assignment.'))

        synopsis_label = QLabel(f'<a href="{synopsis_url}">Project Synopsis</a>')
        synopsis_label.setOpenExternalLinks(True)
        layout.addWidget(synopsis_label)

        source_code_hyperlink = QLabel(f'<a href="{github_url}">Source</a>')
        source_code_hyperlink.setOpenExternalLinks(True)
        layout.addWidget(source_code_hyperlink)

        layout.addWidget(QLabel(f'This software is Free and Open Source Software and is licensed under the <a href="{license_url}">GNU GPLv3</a> license.'))
        layout.addWidget(QLabel(f'Version {version}'))
        layout.addWidget(QLabel(f'Qt {QtCore.qVersion()}'))
        layout.addWidget(QLabel(f'Python {platform.python_version()}'))
        layout.addWidget(QLabel(f'{platform.system()} {platform.release()}'))

        self.setLayout(layout)

