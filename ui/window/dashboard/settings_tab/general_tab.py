from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget, QVBoxLayout
from qt_material import apply_stylesheet, QtStyleTools

from logic.database import Database
from logic.user import UserPrivilege
from ui.helpers.enhanced_controls import ComboBox
from constants import Constants


class GeneralTab(QWidget, QtStyleTools):

    def __init__(self, current_user, current_user_account_settings):
        super(GeneralTab, self).__init__()

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
        self.accent_colour_combo_box.combo_box.setCurrentIndex(
            self.accent_colours.index(self.current_user_account_settings.accent_colour))
        self.accent_colour_combo_box.combo_box.currentIndexChanged.connect(self.change_theme)

        layout.addWidget(self.theme_combo_box)
        layout.addWidget(self.accent_colour_combo_box)

        self.clear_local_connection_settings_button = QPushButton('Clear Connection Settings')
        self.clear_local_connection_settings_button.clicked.connect(self.clear_local_connection_settings)
        self.clear_local_connection_settings_button.setDisabled(Database.is_local_connection_settings_clear())

        layout.addWidget(self.clear_local_connection_settings_button)

        self.logout_button = QPushButton('Logout')
        self.logout_button.setProperty('class', 'danger')
        self.logout_button.clicked.connect(self.restart)

        layout.addWidget(self.logout_button)

        self.reset_button = QPushButton('Reset')
        self.reset_button.setProperty('class', 'danger')
        self.reset_button.clicked.connect(self.reset)

        if current_user.privilege == UserPrivilege.MASTER:
            layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def change_theme(self):
        chosen_theme = self.themes[self.theme_combo_box.combo_box.currentIndex()]
        chosen_accent_colour = self.accent_colours[self.accent_colour_combo_box.combo_box.currentIndex()]

        stylesheet_name = f'{chosen_theme}_{chosen_accent_colour}.xml'
        apply_stylesheet(QApplication.instance(), stylesheet_name)

        self.current_user_account_settings.theme = chosen_theme
        self.current_user_account_settings.accent_colour = chosen_accent_colour
        Database.update_user_account_settings(self.current_user_account_settings)

    def reset(self):
        confirm_delete_box = QMessageBox.warning(self, 'Warning', f'''This will DELETE EVERYTHING - books, users, etc.
No data can be recovered.
Continue?''', QMessageBox.Yes, QMessageBox.No)

        if confirm_delete_box == QMessageBox.Yes:
            Database.delete_database()
            Database.delete_local_database()

            self.restart()

    @staticmethod
    def restart():
        QApplication.closeAllWindows()
        QCoreApplication.exit(Constants.RESTART_RETURN_CODE)

    def clear_local_connection_settings(self):
        Database.clear_local_connection_settings()
        Database.save_local_database()
        self.clear_local_connection_settings_button.setDisabled(True)
