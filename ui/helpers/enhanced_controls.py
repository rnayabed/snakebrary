import os
from PySide2 import QtCore
from PySide2.QtCore import QMargins, QSize, Qt
from PySide2.QtGui import QIcon, QImage, QPixmap
from PySide2.QtWidgets import QFileDialog, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QComboBox, QWidget

class LineEdit(QWidget):

    def __init__(self, info=None, init_value=None, password_mode=False):
        super(LineEdit, self).__init__()

        self.info_label = QLabel(info)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        self.error_label.setAlignment(Qt.AlignRight)

        self.upper = QHBoxLayout()
        self.upper.addWidget(self.info_label)
        self.upper.addWidget(self.error_label)

        self.line_edit = QLineEdit()

        self.line_edit.setText(init_value)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(QMargins(0,0,0,0))
        vbox.addLayout(self.upper)

        lower = QHBoxLayout()
        lower.addWidget(self.line_edit)

        if password_mode:
            self.show_hide_button = QPushButton()
            self.show_hide_button.clicked.connect(self.configure_show_hide_button)
            lower.addWidget(self.show_hide_button)
            self.password_mode_show(False)

        vbox.addLayout(lower)
        vbox.setSpacing(3)

        self.setLayout(vbox)

    def on_error(self, error):
        self.error_label.setText(error)

    def on_success(self):
        self.error_label.clear()
    
    def password_mode_show(self, show):
        self.current_password_mode = show
        if show:
            self.show_hide_button.setText('HIDE')
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.show_hide_button.setText('SHOW')
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)


    def configure_show_hide_button(self):
        self.password_mode_show(not self.current_password_mode)


class PlainTextEdit(QWidget):

    def __init__(self, info, init_value=None):
        super(PlainTextEdit, self).__init__()

        self.info_label = QLabel(info)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        self.error_label.setAlignment(Qt.AlignRight)

        upper = QHBoxLayout()
        upper.addWidget(self.info_label)
        upper.addWidget(self.error_label)

        self.plain_text_edit = QPlainTextEdit()

        self.plain_text_edit.setPlainText(init_value)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        vbox.addLayout(upper)
        vbox.addWidget(self.plain_text_edit)
        vbox.setSpacing(3)

        self.setLayout(vbox)

    def on_error(self, error):
        self.error_label.setText(error)

    def on_success(self):
        self.error_label.clear()


class ComboBox(QWidget):

    def __init__(self, info, l):
        super(ComboBox, self).__init__()

        self.label = QLabel(info)

        self.combo_box = QComboBox()
        self.combo_box.addItems(l)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        hbox.addWidget(self.label)
        hbox.addWidget(self.combo_box)
        hbox.setSpacing(3)

        self.setLayout(hbox)


class FilePicker(QWidget):

    def __init__(self, info, init_value=None, on_select=None, on_clear=None):
        super(FilePicker, self).__init__()

        self.info = info
        self.on_select = on_select
        self.on_clear = on_clear

        self.info_label = QLabel(self.info)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        self.error_label.setAlignment(Qt.AlignRight)

        upper = QHBoxLayout()
        upper.addWidget(self.info_label)
        upper.addWidget(self.error_label)

        self.line_edit = QLineEdit()
        self.line_edit.setEnabled(False)
        self.line_edit.setText(init_value)

        self.select_button = QPushButton('Select')
        self.select_button.clicked.connect(self.__select_file)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.__clear_file)

        lower = QHBoxLayout()
        lower.addWidget(self.line_edit)
        lower.addWidget(self.select_button)
        lower.addWidget(self.clear_button)

        vbox = QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        vbox.addLayout(upper)
        vbox.addLayout(lower)
        vbox.setSpacing(3)

        self.setLayout(vbox)

    def on_error(self, error):
        self.error_label.setText(error)

    def on_success(self):
        self.error_label.clear()

    def __select_file(self):
        img_path = QFileDialog.getOpenFileName(None, 'Open File', os.getcwd(), 'Image Files (*.jpg *.png)')[0]

        if img_path != '':
            self.line_edit.setText(img_path)
            if self.on_select != None:
                self.on_select(img_path)

    def __clear_file(self):
        self.line_edit.clear()
        if self.on_clear != None:
            self.on_clear()


class ImageView(QLabel):

    def __init__(self, info, width, height, style='border: 2px solid black;'):
        super(ImageView, self).__init__()

        self.info = info
        self.style = style

        self.setText(self.info)
        self.setStyleSheet(self.style)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(width, height)
        self.is_clear = True

    def set_image_from_blob(self, blob):
        self.setPixmap(QPixmap.fromImage(QImage.fromData(blob))
                       .scaled(self.width(), self.height(),
                               QtCore.Qt.KeepAspectRatio))
        self.is_clear = False

    def set_image_from_path(self, path):
        self.setPixmap(QPixmap(path).scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.SmoothTransformation))
        self.is_clear = False

    def clear_image(self):
        self.clear()
        self.setText(self.info)
        self.is_clear = True

