from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email):
        self.email = email
        self.id = -1

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_pwdhash(self, pwdhash):
        self.password_hash = pwdhash

    def set_id(self, id):
        self.id = id


