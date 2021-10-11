from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtGui import QFontDatabase, QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QSplashScreen
from logic.database import Database
from qt_material import apply_stylesheet
from mysql.connector import Error
from ui.helpers.helpers import center_screen
from ui.window.connection_details_widget import ConnectionDetailsWidget
from ui.window.login_prompt import LoginPrompt
from ui.window.welcome import Welcome


def start():
    is_fresh_run = True
    try:
        app = QApplication()
    except RuntimeError:
        is_fresh_run = False
        app = QCoreApplication.instance()

    app.setWindowIcon(QIcon('assets/app_icon.png'))
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    if is_fresh_run:
        splash = QSplashScreen(QPixmap('assets/splash.png'))
        splash.show()

    app.processEvents()

    apply_stylesheet(app, theme='light_purple.xml')
    Database.create_local_connection()

    win = decide_window()

    if is_fresh_run:
        splash.finish(win)

    exit_code = app.exec_()

    Database.close_local_connection()
    Database.close_connection()

    if exit_code == 6504:
        start()

def start_connection_details_widget():
    connection_details = ConnectionDetailsWidget(decide_window)
    connection_details.show()
    center_screen(connection_details)
    return connection_details

def decide_window():
    if Database.is_new_local_setup():
        return start_connection_details_widget()
    else:
        if not Database.is_connected() :
            if Database.is_local_connection_settings_clear():
                return start_connection_details_widget()

            try:
                Database.create_connection(Database.get_local_database_server_host(),
                                            Database.get_local_database_server_user(),
                                            Database.get_local_database_server_password(),
                                            Database.get_local_database_server_port())
                return decide_window()
            except Error as e:
                print(e)
                connection_details_widget = start_connection_details_widget()
                connection_details_widget.error_label.setText(e.msg)
                Database.clear_local_connection_settings()
                Database.save_local_database()
                return connection_details_widget
            
        if Database.is_new_server_setup():
            welcome = Welcome()
            welcome.show()
            center_screen(welcome)
            return welcome
        else:
            login_prompt = LoginPrompt()
            login_prompt.show()
            center_screen(login_prompt)
            return login_prompt


if __name__ == '__main__':
    start()