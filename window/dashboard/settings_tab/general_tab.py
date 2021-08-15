from PySide6 import QtCore
from window.helpers.helpers import center_screen
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout
from qt_material import apply_stylesheet, QtStyleTools

from logic.database import Database
from window.helpers.enhanced_controls import ComboBox


class GeneralTab(QWidget, QtStyleTools):

    def __init__(self, app, logout, current_user_account_settings):
        super(GeneralTab, self).__init__()

        self.app = app
        self.logout = logout

        self.current_user_account_settings = current_user_account_settings

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignTop)

        self.themes = [
            'light', 'dark'
        ]

        self.themes_ui = [
            'Light', 'Dark'
        ]

        self.accent_colours = [
            'amber', 'blue', 'cyan', 'lightgreen', 'pink', 'purple', 'red', 'teal', 'yellow'
        ]

        self.accent_colours_ui = [
            'Amber', 'Blue', 'Cyan', 'Light Green', 'Pink', 'Purple', 'Red', 'Teal', 'Yellow'
        ]

        self.theme_combo_box = ComboBox('Theme', self.themes_ui)
        self.theme_combo_box.combo_box.setCurrentIndex(self.themes.index(self.current_user_account_settings.theme))
        self.theme_combo_box.combo_box.currentIndexChanged.connect(self.change_theme)
        self.accent_colour_combo_box = ComboBox('Accent Colour', self.accent_colours_ui)
        self.accent_colour_combo_box.combo_box.setCurrentIndex(self.accent_colours.index(self.current_user_account_settings.accent_colour))
        self.accent_colour_combo_box.combo_box.currentIndexChanged.connect(self.change_theme)

        layout.addLayout(self.theme_combo_box)
        layout.addLayout(self.accent_colour_combo_box)

        self.logout_button = QPushButton('Logout')
        self.logout_button.setProperty('class', 'danger')
        self.logout_button.clicked.connect(self.logout)

        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def change_theme(self):
        chosen_theme = self.themes[self.theme_combo_box.combo_box.currentIndex()]
        chosen_accent_colour = self.accent_colours[self.accent_colour_combo_box.combo_box.currentIndex()]

        stylesheet_name = f'{chosen_theme}_{chosen_accent_colour}.xml'

        print(stylesheet_name)
        apply_stylesheet(self.app, stylesheet_name)

        self.current_user_account_settings.theme = chosen_theme
        self.current_user_account_settings.accent_colour = chosen_accent_colour
        Database.update_user_account_settings(self.current_user_account_settings)
    
