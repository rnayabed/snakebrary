from window.connection_details_widget import ConnectionDetailsWidget
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QScreen

from logic.database import Database
from qt_material import apply_stylesheet

from window.helpers.helpers import center_screen
from window.login_prompt import LoginPrompt

from window.welcome import Welcome

from mysql.connector import Error



def start():
    try:
        app = QApplication()
    except RuntimeError:
        app = QCoreApplication.instance() 
        
    apply_stylesheet(app, theme='light_purple.xml')

    Database.create_local_connection()

    win = decide_window()


    print('Over')
    exit_code = app.exec()
    Database.close_local_connection()
    Database.close_connection()

    if exit_code == 6504:
        start()


def decide_window():
    if Database.is_new_local_setup():
        print('NEW SETUP')
        connection_details = ConnectionDetailsWidget(QApplication.instance(), decide_window)
        connection_details.show()
        center_screen(connection_details) 
        return connection_details
    else:
        print('is Database connected ? ',Database.is_connected())

        print('local db server host: ',Database.get_local_database_server_host())

        if not Database.is_connected():

            try:
                Database.create_connection(Database.get_local_database_server_host(),
                                            Database.get_local_database_server_user(),
                                            Database.get_local_database_server_password(),
                                            Database.get_local_database_server_port())
                
                print('ISSSSSSSSSS Database connected ? ',Database.is_connected())
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