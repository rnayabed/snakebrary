from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QFontDatabase, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
from logic.database import Database
from qt_material import apply_stylesheet
from mysql.connector import Error
from ui.helpers.helpers import center_screen
from ui.window.connection_details_widget import ConnectionDetailsWidget
from ui.window.login_prompt import LoginPrompt
from ui.window.welcome import Welcome


def start():
    try:
        app = QApplication()
    except RuntimeError:
        app = QCoreApplication.instance()

    splash = QSplashScreen(QPixmap('assets/splash.png'))
    splash.show()
    app.processEvents()

    QFontDatabase.addApplicationFont('assets/icons.ttf')

    apply_stylesheet(app, theme='light_purple.xml')
    Database.create_local_connection()


    win = decide_window()

    splash.finish(win)

    exit_code = app.exec()

    Database.close_local_connection()
    Database.close_connection()

    if exit_code == 6504:
        start()


def decide_window():
    if Database.is_new_local_setup():
        connection_details = ConnectionDetailsWidget(decide_window)
        connection_details.show()
        center_screen(connection_details)
        return connection_details
    else:
        if not Database.is_connected():
            try:
                Database.create_connection(Database.get_local_database_server_host(),
                                            Database.get_local_database_server_user(),
                                            Database.get_local_database_server_password(),
                                            Database.get_local_database_server_port())
                return decide_window()
            except Error as e:
                print(e)
                connection_details = ConnectionDetailsWidget(decide_window)
                connection_details.error_label.setText(e.msg)
                connection_details.show()
                center_screen(connection_details)
                return connection_details
            
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