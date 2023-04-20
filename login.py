from flask_login import LoginManager


login_manager = LoginManager()


class User:
    def __init__(self, user_id, password, username):
        self.id = user_id
        self.password = password
        self.username = username









