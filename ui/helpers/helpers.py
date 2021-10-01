from PySide2.QtGui import QIcon, QScreen, QFont
from PySide2.QtWidgets import QApplication, QLayout, QWidget


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


# def delete_widgets_in_layout(layout: QLayout):
#    for i in range(layout.count()):
#        w = layout.itemAt(i)
#        if w is not None:
#            layout.removeWidget(w.widget())


def delete_widgets_in_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())
