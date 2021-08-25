from PySide6.QtGui import QScreen, QFont
from PySide6.QtWidgets import QApplication, QLayout


def center_screen(window):
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = window.frameGeometry()
    geo.moveCenter(center)
    window.move(geo.topLeft())


def get_font_size(size):
    font = QFont()
    font.setPixelSize(size)
    return font


def delete_layouts_in_layout(layout: QLayout):
    for i in range(layout.count()):
        layout.itemAt(i).layout().deleteLater()

class FontAwesomeIcon:
    LOG_OUT = '\ue800 '
    LOG_IN = '\ue801 '
    SERVER = '\uf233 '
    REFRESH = '\ue802 '
    PLUS = '\ue803 '
    KEY = '\ue804 '
    EDIT = '\ue805 '
    TRASH = '\uf1f8 '
    FILE = '\ue806 '
    EYE = '\ue807 '
    EYE_SLASH = '\ue808 '
    STAR = '\ue809 '
    STAR_EMPTY = '\ue80a '
    STAR_HALF = '\uf123 '