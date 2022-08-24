from distutils.log import debug
from flask import Flask
from flask_mysqldb import MySQL
from flask_migrate import Migrate
from flask_login import LoginManager 

app = Flask(__name__)

app.secret_key = 'this1sKey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)
migrate = Migrate(app, mysql)

"""
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
"""

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
