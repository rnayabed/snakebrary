from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QScreen

from logic.database import Database
from qt_material import apply_stylesheet

from window.helpers.helpers import center_screen
from window.login_prompt import LoginPrompt

from window.welcome import Welcome



def start():
    try:
        app = QApplication()
    except RuntimeError:
        app = QCoreApplication.instance() 
        
    #QFontDatabase.addApplicationFont("Roboto/Roboto-Regular.ttf")
    apply_stylesheet(app, theme='light_purple.xml')

    Database.create_connection()

    if Database.is_new_setup():
        welcome = Welcome(app)
        welcome.show()
        center_screen(welcome)
    else:
        login_prompt = LoginPrompt(app)
        login_prompt.show()
        center_screen(login_prompt)

    exit_code = app.exec()
    Database.close_connection()

    if exit_code == 6504:
        start()
    

if __name__ == '__main__':
    start()