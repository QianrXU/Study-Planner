from distutils.log import debug
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

app = Flask(__name__)

app.secret_key = 'this1sKey'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:password123@localhost/study_planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'


from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)

