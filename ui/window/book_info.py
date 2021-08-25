from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget

from logic.book import BookHolder
from logic.database import Database
from logic.user import User, UserPrivilege
from ui.helpers.enhanced_controls import ImageView
from ui.helpers.helpers import FontAwesomeIcon, get_font_size, center_screen
from ui.layouts_and_widgets.book_ratings_widget import BookRatingsWidget
from ui.window.book_holders_window import BookHoldersWindow
from ui.window.book_reviewers_window import BookReviewersWindow
from ui.window.book_wizard_window import BookWizardWindow


class BookInfo(QDialog):

    def __init__(self, book, dashboard_on_books_edited, current_user: User, parent=None):
        super(BookInfo, self).__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)

        self.book = book
        self.dashboard_on_books_edited = dashboard_on_books_edited
        self.current_user = current_user

        self.setWindowTitle("Book Information")
        self.resize(800, 700)

        main_vbox = QVBoxLayout()
        main_vbox.setAlignment(QtCore.Qt.AlignTop)

        hbox_1 = QHBoxLayout()
        hbox_1.setSpacing(10)

        self.cover_photo = ImageView('Cover Photo', 300, 300)
        hbox_1.addWidget(self.cover_photo)

        self.name_label = QLabel()
        self.name_label.setFont(get_font_size(30))

        self.author_label = QLabel()
        self.author_label.setFont(get_font_size(17))

        self.genres_label = QLabel()

        self.isbn_label = QLabel()
        self.price_label = QLabel()

        self.date_time_added_label = QLabel()
        self.current_holder_label = QLabel()
        size_policy = self.current_holder_label.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.current_holder_label.setSizePolicy(size_policy)

        self.get_return_button = QPushButton()

        self.get_book_holders_details = QPushButton('book holders list')
        self.get_book_holders_details.clicked.connect(self.show_book_holders_list_window)

        self.get_book_reviewers_details = QPushButton('book reviewers')
        self.get_book_reviewers_details.clicked.connect(self.show_book_reviewers_list_window)

        show_book_holders_reviewers_hbox = QHBoxLayout()
        show_book_holders_reviewers_hbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        show_book_holders_reviewers_hbox.addWidget(self.get_book_holders_details)
        show_book_holders_reviewers_hbox.addWidget(self.get_book_reviewers_details)

        self.edit_book_button = QPushButton(FontAwesomeIcon.EDIT+'Edit')
        self.edit_book_button.clicked.connect(self.on_edit_button_clicked)

        self.delete_book_button = QPushButton(FontAwesomeIcon.TRASH+'Delete')
        self.delete_book_button.setProperty('class', 'danger')
        self.delete_book_button.clicked.connect(self.on_delete_button_clicked)

        edit_delete_button_hbox = QHBoxLayout()
        edit_delete_button_hbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        edit_delete_button_hbox.addWidget(self.edit_book_button)
        edit_delete_button_hbox.addWidget(self.delete_book_button)

        non_normal_buttons_vbox = QVBoxLayout()
        non_normal_buttons_vbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        non_normal_buttons_vbox.addLayout(show_book_holders_reviewers_hbox)
        non_normal_buttons_vbox.addLayout(edit_delete_button_hbox)

        self.non_normal_buttons_widget = QWidget()
        self.non_normal_buttons_widget.setLayout(non_normal_buttons_vbox)

        vbox_labels_1 = QVBoxLayout()
        vbox_labels_1.setAlignment(QtCore.Qt.AlignTop)
        vbox_labels_1.addWidget(self.name_label)
        vbox_labels_1.addWidget(self.author_label)
        vbox_labels_1.addWidget(self.genres_label)
        vbox_labels_1.addWidget(self.isbn_label)
        vbox_labels_1.addWidget(self.price_label)
        vbox_labels_1.addWidget(self.date_time_added_label)
        vbox_labels_1.addWidget(self.current_holder_label)
        vbox_labels_1.addWidget(self.get_return_button)
        vbox_labels_1.addWidget(self.non_normal_buttons_widget)

        hbox_1.addLayout(vbox_labels_1)

        main_vbox.addLayout(hbox_1)

        self.ratings_widget = BookRatingsWidget(self.book, self.current_user)
        self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        main_vbox.addWidget(self.ratings_widget)

        self.about_label_header = QLabel('About')
        self.about_label_header.setContentsMargins(QtCore.QMargins(0, 10, 0, 0))
        self.about_label_header.setFont(get_font_size(18))

        self.about_label = QLabel()
        self.about_label.setAlignment(QtCore.Qt.AlignJustify)
        self.about_label.setWordWrap(True)

        self.about_label_scroll_area = QScrollArea()
        self.about_label_scroll_area.setWidgetResizable(True)
        self.about_label_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.about_label_scroll_area.setWidget(self.about_label)

        about_layout = QVBoxLayout()
        about_layout.addWidget(self.about_label_header)
        about_layout.addWidget(self.about_label_scroll_area)

        self.about_widget = QWidget()
        self.about_widget.setLayout(about_layout)

        main_vbox.addWidget(self.about_widget)

        self.setLayout(main_vbox)
        self.configure_ui()

    def configure_ui(self):
        if self.book.photo == None:
            self.cover_photo.clear_image()
            self.cover_photo.hide()
        else:
            self.cover_photo.set_image_from_blob(self.book.photo)
            self.cover_photo.show()

        self.name_label.setText(self.book.name)
        self.author_label.setText(f'by {self.book.author}')

        if len(self.book.genres) == 1:
            self.genres_label.setText('Genre: ' + self.book.get_stylish_genres())
        else:
            self.genres_label.setText('Genres: ' + self.book.get_stylish_genres())

        self.isbn_label.setText(f'ISBN: {self.book.ISBN}')
        self.price_label.setText(f'Price: ₹ {self.book.price}')

        if self.book.about != '':
            self.about_label.setText(self.book.about)
            self.about_widget.show()
        else:
            self.about_widget.hide()

        self.configure_get_return_button()

        if self.current_user.privilege == UserPrivilege.NORMAL:
            self.current_holder_label.hide()
            self.date_time_added_label.hide()
            self.non_normal_buttons_widget.hide()
        else:
            self.date_time_added_label.setText(f'Date/Time added: {self.book.date_time_added}')
            self.configure_current_holder_label()

        self.ratings_widget.reload(self.book)

    def on_delete_button_clicked(self):
        warning_box = QMessageBox.warning(self, 'Warning', f'''Are you sure you want to delete the following book
Name: {self.book.name}
Author: {self.book.author}
ISBN: {self.book.ISBN}
Date Time Added: {self.book.date_time_added}''', QMessageBox.Yes, QMessageBox.No)

        if warning_box == QMessageBox.Yes:
            Database.delete_book(self.book.ISBN)
            self.dashboard_on_books_edited()
            self.close()

    def get_book(self):
        self.get_return_button.setDisabled(True)

        new_holder = BookHolder(self.current_user.username)
        self.book.holders.append(new_holder.get_raw_list())
        Database.update_book_holders(self.book.holders, self.book.ISBN)

        self.configure_get_return_button()
        self.get_return_button.setDisabled(False)
        self.configure_current_holder_label()
    
    def configure_current_holder_label(self):
        current_holder = self.book.get_current_holder()
        if current_holder == None:
            self.current_holder_label.hide()
        else:
            current_holder_user = Database.get_user_by_username(current_holder)
            self.current_holder_label.setText(f'Current Holder: {current_holder} ({current_holder_user.name})')
            self.current_holder_label.show()

    def return_book(self):
        
        self.get_return_button.setDisabled(True)
        self.book.return_now()
        Database.update_book_holders(self.book.holders, self.book.ISBN)

        self.configure_get_return_button()
        self.ratings_widget.reload(self.book)
        self.get_return_button.setDisabled(False)
        self.configure_current_holder_label()

    def configure_get_return_button(self):
        self.disconnect_slots_get_return_button()

        if self.book.get_current_holder() == None:
            self.get_return_button.setText('Get it')
            self.get_return_button.clicked.connect(self.get_book)
        else:
            current_holder_privilege = Database.get_user_by_username(self.book.get_current_holder()).privilege
            if self.book.get_current_holder() == self.current_user.username or (self.current_user.privilege != UserPrivilege.NORMAL and current_holder_privilege != self.current_user.privilege and current_holder_privilege != UserPrivilege.MASTER):
                self.get_return_button.setText('Return')
                self.get_return_button.clicked.connect(self.return_book)
            else:
                self.get_return_button.setDisabled(True)
                self.get_return_button.setText('Unavailable')

    def disconnect_slots_get_return_button(self):
        try:
            self.get_return_button.clicked.disconnect()
        except:
            pass

    def show_book_holders_list_window(self):
        self.book_holders_list_window = BookHoldersWindow(self.book.holders, self.current_user, self)
        self.book_holders_list_window.exec()
        center_screen(self.book_holders_list_window)

    def on_edit_button_clicked(self):
        self.book_wizard_window = BookWizardWindow(self.on_book_edited, self.book, self)
        self.book_wizard_window.exec()
        center_screen(self.book_wizard_window)

    def on_book_edited(self):
        self.dashboard_on_books_edited()
        self.book = Database.get_book_by_ISBN(self.book.ISBN)
        self.configure_ui()

    def show_book_reviewers_list_window(self):
        self.book_reviewers_list_window = BookReviewersWindow(self.book, self.current_user, self.configure_ui, self)
        self.book_reviewers_list_window.exec()
        center_screen(self.book_reviewers_list_window)
