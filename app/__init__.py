# Adapted codes based on: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

from distutils.log import debug
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
import os

app = Flask(__name__)

app.secret_key = 'this1sKey'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'


from app import routes, models, forms

if __name__ == '__main__':
    app.run(debug=True)

