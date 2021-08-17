from PySide6 import QtWidgets
from window.dashboard.book_ratings_layout import BookRatingsLayout
from logic.user import User, UserPrivilege
from logic.database import Database
from os import name
from window.helpers.helpers import get_font_size
from window.helpers.enhanced_controls import ImageView
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from logic.book import Book, BookHolder
from PySide6.QtWidgets import (QAbstractScrollArea, QDialog, QHBoxLayout, QLabel, QPushButton, QScrollArea, QTableWidget, QVBoxLayout, QWidget, QTabWidget)
from qt_material import apply_stylesheet, QtStyleTools


class BookHoldersWindow(QDialog):

    def __init__(self, book_holders, parent=None):
        super(BookHoldersWindow, self).__init__(parent)
        
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.book_holders = book_holders

        self.setWindowTitle("Book Holders")
        self.resize(800,600)
        
        self.book_holders_table = QTableWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.book_holders_table)

        self.setLayout(vbox)

        print('book holdersss : ',book_holders)

        self.configure_table()
    
    def configure_table(self):
        self.book_holders_table.setSortingEnabled(True)
        self.book_holders_table.setRowCount(len(self.book_holders))
        self.book_holders_table.setColumnCount(4) 
        self.book_holders_table.setHorizontalHeaderLabels(["Username", "Name", "   Issued On   ", "   Returned On   "])

        self.book_holders_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.book_holders_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        
        self.book_holders_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.book_holders_table.verticalHeader().setDefaultSectionSize(70)


        for i in range(len(self.book_holders)):
            each_holder = self.book_holders[i]
            
            username_widget = QLabel(each_holder[0])
            name_widget = QLabel(Database.get_users_by_username(each_holder[0])[0].name)
            issued_on_widget = QLabel(each_holder[1])
            returned_on_widget = QLabel(each_holder[2])

            self.book_holders_table.setCellWidget(i, 0, username_widget)
            self.book_holders_table.setCellWidget(i, 1, name_widget)
            self.book_holders_table.setCellWidget(i, 2, issued_on_widget)
            self.book_holders_table.setCellWidget(i, 3, returned_on_widget)





