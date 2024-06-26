from datetime import datetime


class UserPrivilege:
    MASTER = 0
    ADMIN = 1
    NORMAL = 2

    @staticmethod
    def get_ui_name(user_privilege):
        if user_privilege == UserPrivilege.MASTER:
            return 'Master'
        elif user_privilege == UserPrivilege.ADMIN:
            return 'Administrator'
        elif user_privilege == UserPrivilege.NORMAL:
            return 'Normal'


class UserSettings:
    def __init__(self, username, theme, accent_colour):
        self.username = username
        self.theme = theme
        self.accent_colour = accent_colour


class User:
    def __init__(self, username, password, password_hint, name, is_disabled=False,
                 privilege=UserPrivilege.NORMAL, photo=None, date_time_created=None):
        self.username = username
        self.password = password
        self.password_hint = password_hint
        self.name = name
        self.is_disabled = is_disabled
        self.privilege = privilege
        self.photo = photo

        if date_time_created is None:
            date_time_created = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.date_time_created = date_time_created
