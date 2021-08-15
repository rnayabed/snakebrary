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