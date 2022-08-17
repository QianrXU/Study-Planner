from app import mysql
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)