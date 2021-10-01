from PySide2 import QtCore
from PySide2.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QPushButton, QSlider, QVBoxLayout, QWidget
import os
from logic.book import Book
from logic.database import Database
from logic.user import User
from ui.helpers.helpers import get_font_size, delete_widgets_in_layout

import qtawesome as qta


class BookRatingsWidget(QWidget):

    def __init__(self, book: Book, current_user: User):
        super(BookRatingsWidget, self).__init__(None)

        self.book = book
        self.current_user = current_user

        header_label = QLabel('Ratings')
        header_label.setContentsMargins(QtCore.QMargins(0, 10, 0, 0))
        header_label.setFont(get_font_size(18))

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(header_label)

        overview_hbox = QHBoxLayout()

        self.large_rating_label = QLabel()
        self.large_rating_label.setContentsMargins(QtCore.QMargins(0, 0, 50, 0))
        self.large_rating_label.setFont(get_font_size(35))

        # self.rating_graphic_label = QLabel()
        # self.rating_graphic_label.setFont(get_font_size(20))
        # self.rating_graphic_label.setStyleSheet(f'color: {primary_color}')

        self.primary_color = os.environ.get('QTMATERIAL_PRIMARYCOLOR')

        self.rating_graph_hbox = QHBoxLayout()

        self.total_ratings_label = QLabel()
        self.total_ratings_label.setFont(get_font_size(14))

        left_rating_layout = QVBoxLayout()
        left_rating_layout.addWidget(self.large_rating_label)
        left_rating_layout.addLayout(self.rating_graph_hbox)
        left_rating_layout.addWidget(self.total_ratings_label)

        overview_hbox.addLayout(left_rating_layout)

        right_layout_vbox = QVBoxLayout()

        self.rating_progress_bar_5 = RatingProgressBar(5)
        self.rating_progress_bar_4 = RatingProgressBar(4)
        self.rating_progress_bar_3 = RatingProgressBar(3)
        self.rating_progress_bar_2 = RatingProgressBar(2)
        self.rating_progress_bar_1 = RatingProgressBar(1)

        right_layout_vbox.addLayout(self.rating_progress_bar_5)
        right_layout_vbox.addLayout(self.rating_progress_bar_4)
        right_layout_vbox.addLayout(self.rating_progress_bar_3)
        right_layout_vbox.addLayout(self.rating_progress_bar_2)
        right_layout_vbox.addLayout(self.rating_progress_bar_1)

        overview_hbox.addLayout(right_layout_vbox)

        self.vbox.addLayout(overview_hbox)

        self.rating_slider = QSlider(QtCore.Qt.Horizontal)
        self.rating_slider.setMinimum(1)
        self.rating_slider.setMaximum(5)
        self.rating_slider.setTickInterval(1)

        self.rating_slider_status_label = QLabel('1')

        self.rating_slider.valueChanged.connect(self.rating_slider_value_changed)

        self.submit_rating_button = QPushButton('Submit Rating')
        self.submit_rating_button.clicked.connect(self.submit_rating_button_clicked)

        self.delete_rating_button = QPushButton('Delete Rating')
        self.delete_rating_button.setProperty('class', 'danger')
        self.delete_rating_button.clicked.connect(self.delete_rating_button_clicked)

        rating_layout = QVBoxLayout()

        rating_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        self.rating_current_status_label = QLabel()
        rating_layout.addWidget(self.rating_current_status_label)

        rating_layout_hbox = QHBoxLayout()
        rating_layout_hbox.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        rating_layout_hbox.addWidget(self.rating_slider)
        rating_layout_hbox.addWidget(self.rating_slider_status_label)
        rating_layout_hbox.addWidget(self.submit_rating_button)
        rating_layout_hbox.addWidget(self.delete_rating_button)

        rating_layout.addLayout(rating_layout_hbox)

        self.rating_layout_widget = QWidget()
        self.rating_layout_widget.setLayout(rating_layout)

        self.vbox.addWidget(self.rating_layout_widget)

        self.setLayout(self.vbox)

        self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        self.configure_ui()

    def rating_slider_value_changed(self):
        self.rating_slider_status_label.setText(str(self.rating_slider.value()))

    def delete_rating_button_clicked(self):
        self.book_ratings.delete_rating_by_username(self.current_user.username)
        Database.update_book_ratings(self.book_ratings)
        self.configure_ui()

    def submit_rating_button_clicked(self):
        self.book_ratings.set_rating_by_username(self.current_user.username, self.rating_slider.value())
        Database.update_book_ratings(self.book_ratings)
        self.configure_ui()

    def reload(self, book):
        self.book = book
        self.configure_ui()

    def configure_ui(self):
        self.book_ratings = Database.get_book_ratings(self.book.ISBN)
        average_rating = self.book_ratings.get_average_rating()
        self.large_rating_label.setText(str(average_rating))

        # self.rating_graph_hbox.setText(self.get_rating_graphic(average_rating))

        self.set_rating_graphic(average_rating)

        if len(self.book_ratings.ratings) == 1:
            self.total_ratings_label.setText(f'{len(self.book_ratings.ratings)} rating')
        else:
            self.total_ratings_label.setText(f'{len(self.book_ratings.ratings)} ratings')

        self.rating_progress_bar_1.load(self.book_ratings)
        self.rating_progress_bar_2.load(self.book_ratings)
        self.rating_progress_bar_3.load(self.book_ratings)
        self.rating_progress_bar_4.load(self.book_ratings)
        self.rating_progress_bar_5.load(self.book_ratings)

        if not self.book.is_eligible_to_rate(self.current_user.username):
            self.rating_layout_widget.hide()
        else:
            self.rating_layout_widget.show()
            existing_rating = self.book_ratings.get_rating_by_username(self.current_user.username)

            if existing_rating == None:
                self.rating_current_status_label.setText(
                    'You have read but not rated this book yet. Go ahead and rate it!')
                self.delete_rating_button.hide()
            else:
                self.rating_current_status_label.setText(f'You have rated this book {existing_rating} out of 5')
                self.rating_slider.setValue(existing_rating)
                self.delete_rating_button.show()

    def get_rating_progress_bar_for_rating(self, rating):
        rate_label = QLabel(str(rating))
        rating_bar = QProgressBar()

        if len(self.book_ratings.ratings) == 0:
            rating_bar.setValue(0)
        else:
            rating_bar.setValue(self.book_ratings.get_ratings_by_proportion(rating))

        hbox = QHBoxLayout()
        hbox.addWidget(rate_label)
        hbox.addWidget(rating_bar)
        return hbox

    def set_rating_graphic(self, rating):
        rating_broken = str(rating).split('.')
        major = int(rating_broken[0])
        minor = int(rating_broken[1])

        delete_widgets_in_layout(self.rating_graph_hbox)

        for i in range(major):
            self.rating_graph_hbox.addWidget(self.get_label_with_icon('mdi.star'))

        if major == 5:
            return

        if minor >= 5:
            self.rating_graph_hbox.addWidget(self.get_label_with_icon('mdi.star-half-full'))
        else:
            self.rating_graph_hbox.addWidget(self.get_label_with_icon('mdi.star-outline'))

        for i in range(4 - major):
            self.rating_graph_hbox.addWidget(self.get_label_with_icon('mdi.star-outline'))

    def get_label_with_icon(self, icon_code):
        label = QLabel()
        label.setPixmap(qta.icon(icon_code, color=self.primary_color).pixmap(32))
        return label


class RatingProgressBar(QHBoxLayout):

    def __init__(self, rating):
        super(RatingProgressBar, self).__init__(None)

        self.rating = rating
        self.rate_label = QLabel(str(self.rating))
        self.rating_bar = QProgressBar()

        self.addWidget(self.rate_label)
        self.addWidget(self.rating_bar)

    def load(self, book_ratings):
        if len(book_ratings.ratings) == 0:
            self.rating_bar.setValue(0)
        else:
            self.rating_bar.setValue(book_ratings.get_ratings_by_proportion(self.rating))
